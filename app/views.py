from django.shortcuts import render, redirect
from app.models import Airport, AirportRoute
from app.forms import AirportForm, AirportRouteForm, AddRouteSimpleForm, ShortestRouteForm, NthRouteForm


def add_airport(request):
    form = AirportForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('route_list')
    return render(request, 'add_airport.html', {'form': form})


def add_route(request):
    form = AddRouteSimpleForm(request.POST or None)
    if form.is_valid():
        source_code = form.cleaned_data['source_code'].strip().upper()
        destination_code = form.cleaned_data['destination_code'].strip().upper()
        position = form.cleaned_data['position']
        distance_km = form.cleaned_data['distance_km']

        source, _ = Airport.objects.get_or_create(code=source_code)
        destination, _ = Airport.objects.get_or_create(code=destination_code)

        AirportRoute.objects.create(
            source=source,
            destination=destination,
            position=position,
            distance_km=distance_km,
        )

        return redirect('route_list')

    return render(request, 'add_route.html', {'form': form})


def _get_tree_node(airport):
    left_route = AirportRoute.objects.filter(source=airport, position=AirportRoute.POSITION_LEFT).first()
    right_route = AirportRoute.objects.filter(source=airport, position=AirportRoute.POSITION_RIGHT).first()

    return {
        'airport': airport,
        'left': _get_tree_node(left_route.destination) if left_route else None,
        'left_route': left_route,
        'right': _get_tree_node(right_route.destination) if right_route else None,
        'right_route': right_route,
    }


def route_tree(request):
    roots = Airport.objects.filter(incoming_routes__isnull=True)
    tree = [_get_tree_node(root) for root in roots]
    return render(request, 'tree.html', {'tree': tree})


def route_list(request):
    routes = AirportRoute.objects.select_related('source', 'destination').all()
    airports = Airport.objects.all()
    return render(request, 'route_list.html', {'routes': routes, 'airports': airports})


def longest_route(request):
    route = AirportRoute.objects.order_by('-distance_km').first()
    return render(request, 'longest.html', {'route': route})


def _find_shortest_path(start, end):
    import heapq

    distances = {start: 0}
    prev = {}
    queue = [(0, start)]
    seen = set()

    while queue:
        current_distance, airport = heapq.heappop(queue)
        if airport in seen:
            continue
        seen.add(airport)
        if airport == end:
            break

        # Only traverse forward direction (source -> destination) for tree structure
        for route in AirportRoute.objects.filter(source=airport):
            neighbor = route.destination
            total = current_distance + route.distance_km
            if total < distances.get(neighbor, float('inf')):
                distances[neighbor] = total
                prev[neighbor] = (airport, route)
                heapq.heappush(queue, (total, neighbor))

    if end not in distances:
        return None

    path = []
    at = end
    while at != start:
        parent, route = prev.get(at, (None, None))
        if parent is None:
            break
        path.append({'route': route, 'airport': at})
        at = parent
    path.reverse()

    return {
        'distance': distances[end],
        'path': path,
        'start': start,
        'end': end,
    }


def shortest_route(request):
    result = None
    form = ShortestRouteForm(request.POST or None)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        result = _find_shortest_path(start, end)
    return render(request, 'shortest.html', {
        'form': form,
        'result': result,
    })


def _find_nth_node(start, direction, n):
    current = start
    for _ in range(n):
        route = AirportRoute.objects.filter(source=current, position=direction).first()
        if not route:
            return None
        current = route.destination
    return current


def nth_route(request):
    result = None
    form = NthRouteForm(request.POST or None)

    if form.is_valid():
        start = form.cleaned_data['start']
        direction = form.cleaned_data['direction']
        n = form.cleaned_data['n']
        node = _find_nth_node(start, direction, n)
        result = {
            'start': start,
            'direction': direction,
            'n': n,
            'airport': node,
            'message': 'No airport found at this depth' if not node else None,
        }

    return render(request, 'nth_route.html', {
        'form': form,
        'result': result,
    })


