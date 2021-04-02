from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def get_paginator(querySet, queryType, page=1, limit=10):
    paginator = Paginator(querySet, limit)

    try:
        page_object = paginator.page(page)
        result = page_object.object_list

    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
        result = None

    return queryType(
        page=page_object.number,
        pages=paginator.num_pages,
        count=paginator.count,
        has_next=page_object.has_next(),
        has_prev=page_object.has_previous(),
        result=result
    )