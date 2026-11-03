
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

from config.paths_config import MODEL_SAVE_PATH

app = FastAPI(title="Airline Satisfaction Prediction")

# Serve CSS and other static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the trained model once
model = joblib.load(MODEL_SAVE_PATH)

# Configure HTML templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": None,
            "error": None
        }
    )


@app.post("/", response_class=HTMLResponse)
async def predict(
    request: Request,
    departure_delay: float = Form(..., alias="Departure Delay"),
    arrival_delay: float = Form(..., alias="Arrival Delay"),
    flight_distance: float = Form(..., alias="Flight Distance"),
    online_boarding: int = Form(..., alias="Online Boarding"),
    wifi_service: int = Form(..., alias="Inflight wifi service"),
    travel_class: int = Form(..., alias="Class"),
    travel_type: int = Form(..., alias="Type of Travel"),
    entertainment: int = Form(..., alias="Inflight entertainment"),
    seat_comfort: int = Form(..., alias="Seat comfort"),
    leg_room: int = Form(..., alias="Leg room service"),
    onboard_service: int = Form(..., alias="On-board service"),
    cleanliness: int = Form(..., alias="Cleanliness"),
    online_booking: int = Form(..., alias="Ease of Online Booking"),
):
    try:
        # Calculate the engineered feature
        delay_ratio = (
            departure_delay + arrival_delay
        ) / (flight_distance + 1)

        # Keep the exact feature order used during training
        data = [[
            online_boarding,
            delay_ratio,
            wifi_service,
            travel_class,
            travel_type,
            flight_distance,
            entertainment,
            seat_comfort,
            leg_room,
            onboard_service,
            online_booking,
            cleanliness,
        ]]

        prediction = int(model.predict(data)[0])

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "prediction": prediction,
                "error": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "prediction": None,
                "error": str(e)
            },
            status_code=500
        )
