from string import ascii_letters
from string import digits
from string import punctuation

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from passlib.context import CryptContext

from watch_n_learn.authentication.main import load_user
from watch_n_learn.authentication.main import manager
from watch_n_learn.database.main import session
from watch_n_learn.database.models import User
from watch_n_learn.helper.parse import body_to_json
from watch_n_learn.helper.template import flash

guest_post_router = APIRouter(prefix="/internal")

hashing_context = CryptContext(schemes=["bcrypt"])

@guest_post_router.post("/login")
async def login(request_: Request) -> RedirectResponse:

    body = await body_to_json(request_, ["username", "password"])

    if not body:
        flash(request_, "Missing fields")

    if isinstance(body, str):
        flash(request_, f"'{body.capitalize()}' field cannot be empty")

        return RedirectResponse("/login", status.HTTP_302_FOUND)

    username = body["username"].strip()

    user = load_user(username)

    if user is None:
        flash(request_, "Invalid username")

        return RedirectResponse("/login", status.HTTP_302_FOUND)

    if not hashing_context.verify(body["password"].strip(), user.hashed_password):
        flash(request_, "Incorrect password")

        return RedirectResponse("/login", status.HTTP_302_FOUND)

    response = RedirectResponse("/", status.HTTP_302_FOUND)

    response.set_cookie("authentication_token", manager.create_access_token(data={"sub": username}))

    flash(request_, "Logged in")

    return response

@guest_post_router.post("/sign-up")
async def sign_up(request_: Request) -> RedirectResponse:

    body = await body_to_json(request_, ["name", "username", "password", "confirm_password"])

    if not body:
        flash(request_, "Missing fields")

    if isinstance(body, str):
        empty_field = body.capitalize()
        if body == "name":
            empty_field = "Full name"
        elif body == "confirm_password":
            empty_field = "Confirm password"
        flash(request_, f"'{empty_field}' field can't be empty")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    name_ = body["name"].strip()
    username_ = body["username"].strip()
    password = body["password"]

    if name_.count(" ") != 1:
        flash(request_, "Name should be in the format [first name <space> last name]")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    if len(name_) > 64:
        flash(request_, "Length of name should be shorter than 64 characters")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    username_length = len(username_)

    if username_length < 6 or username_length > 16:
        flash(request_, "Length of username should be between 6 and 16 characters")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    ALLOWED_USERNAME_CHARACTERS = set(ascii_letters + digits)

    for character in username_:
        if character not in ALLOWED_USERNAME_CHARACTERS:
            flash(request_, "Username should only include letters and digits")

            return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    if load_user(username_) is not None:
        flash(request_, "Username has already been taken")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    password_length = len(password)

    if password_length < 6 or password_length > 16:
        flash(request_, "Length of password should be between 6 and 16 characters")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    ALLOWED_PASSWORD_CHARACTERS = set(ascii_letters + digits + punctuation)

    for character in password:
        if character not in ALLOWED_PASSWORD_CHARACTERS:
            flash(request_, "Password should only include letters, digits and punctuation")

            return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    if body["confirm_password"] != password:
        flash(request_, "Confirm password does not match password")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    user = User(name=name_, username=username_, hashed_password=hashing_context.hash(password))

    session.add(user)

    session.commit()

    session.expire(user)

    response = RedirectResponse("/", status.HTTP_302_FOUND)

    response.set_cookie(
        "authentication_token", manager.create_access_token(data={"sub": username_})
    )

    flash(request_, "You have signed up")

    return response
