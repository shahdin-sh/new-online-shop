from django import template

register = template.Library()

@register.filter
# comments comes from our view ------> comments = product_detail.comments.filter(parent=None).order_by('-datetime_created')
def only_active_comments(comments):
    return comments.filter(is_active=True) # comments.exclude(active=False) 
