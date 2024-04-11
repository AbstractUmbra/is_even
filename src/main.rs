#[macro_use]
extern crate rocket;

use std::ops::Rem;

use rocket::{
    fs::{relative, FileServer},
    serde::{json::Json, Serialize},
};

#[derive(Responder)]
#[response(status = 418, content_type = "json")]
struct FunnyError(&'static str);

#[derive(Serialize)]
#[serde(crate = "rocket::serde")]
struct EvenResult {
    number: f64,
    is_even: bool,
}

#[get("/<number>")]
async fn is_even(number: f64) -> Result<Json<EvenResult>, FunnyError> {
    if number.is_nan() || number.is_infinite() {
        return Err(FunnyError(
            "{\"message\": \"This is how you get your rocks off? Pervert.\"}",
        ));
    }

    let rem = number.rem(2.0);

    let even = rem == 0.0;

    Ok(Json(EvenResult {
        number,
        is_even: even,
    }))
}

#[rocket::main]
async fn main() -> Result<(), rocket::Error> {
    let _ = rocket::build()
        .mount("/", routes![is_even])
        .mount("/", FileServer::from(relative!("static/images")))
        .launch()
        .await?;

    Ok(())
}
