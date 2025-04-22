
def current_user(request):
    return {"user": request.session.get("user")}
