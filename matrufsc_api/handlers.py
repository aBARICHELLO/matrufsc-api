from aiohttp import web

from .utils import query_check, filter_dicts, clean_dicts


def json_response(*args, **kwargs):
    return web.json_response(
        *args,
        headers={
            'Access-Control-Allow-Origin': '*',
            **kwargs.pop('headers', {})
        },
        **kwargs
    )


@query_check(optional=['semester', 'campus'])
async def courses(request: web.Request):
    query_semester = request.query.get('semester')
    query_campus = request.query.get('campus')

    data = (
        {
            'semester': semester,
            'campus': campus,
            'id': course_id,
            'name': course['course_name'],
            'class_hours': course['class_hours'],
        }
        for semester, campi in request.app['database'].items()
        for campus, courses in campi.items()
        for course_id, course in courses.items()
    )

    if query_semester is not None:
        data = filter_dicts(data, 'semester', query_semester)

    if query_campus is not None:
        data = filter_dicts(data, 'campus', query_campus)

    data = clean_dicts(data, ['semester', 'campus'])

    return json_response(list(data), headers={})


@query_check(required=['course_id'], optional=['semester'])
async def classes(request: web.Request):
    query_course_id = request.query.get('course_id')
    query_semester = request.query.get('semester')

    data = (
        {
            'course_id': course_id,
            'semester': semester,
            'class_id': class_id,
            **class_info,
        }
        for semester, campi in request.app['database'].items()
        for campus, courses in campi.items()
        for course_id, course in courses.items()
        for class_id, class_info in course['classes'].items()
    )

    if query_course_id is not None:
        data = filter_dicts(data, 'course_id', query_course_id)

    if query_semester is not None:
        data = filter_dicts(data, 'semester', query_semester)

    data = clean_dicts(data, ['course_id', 'semester'])

    return json_response(list(data))
