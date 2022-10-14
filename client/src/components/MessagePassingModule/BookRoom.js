import "./BookRoom.css";
import { useNavigate } from "react-router-dom";
import rentimage from "../../assets/images/BookRoom.png";
import DatePicker from "react-date-picker";
import React, { useState } from "react";
import { format } from 'date-fns';
import axios from "axios";
import { getHotelUrl } from "../getUrl";

const BookRoom = () => {
  const navigate = useNavigate();

  const [checkIn, setCheckIn] = useState(new Date());
  const [checkOut, setCheckOut] = useState(new Date());

  const onClick = () => {
    let data = JSON.stringify({
      "checkin_date": format(checkIn, 'yyyy/MM/dd'),
      "checkout_date": format(checkOut, 'yyyy/MM/dd')
    });
    console.log("data====");
    console.log(data);
    
    let config = {
      method: 'post',
      url: getHotelUrl()+'/get_available_rooms',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    };
    
    axios(config)
    .then(function (response) {
      console.log(JSON.stringify(response.data));
      console.log(checkIn);
      console.log(checkOut);
      navigate("/availablerooms", {'state':{'rooms':JSON.stringify(response.data), 'checkin_date':format(checkIn, 'yyyy/MM/dd'), 'checkout_date':format(checkOut, 'yyyy/MM/dd')}});
    })
    .catch(function (error) {
      console.log(error);
    });
    
  };

  const bookings = () => {
    navigate("/bookings")
  }

  return (
    <div className="form-container row">
      <div className="col-md-6">
        <img src={rentimage} width="90%" />
      </div>
      <div className="col-md-6">
      <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={bookings}
            >
            View Bookings
            </button>
          </center>
        </div>
        <div className="hotel-booking">
          <h1>Hotel Booking</h1>
        </div>
        <div className="checkin-date">
          <h5>Check-in Date</h5>{" "}
          <DatePicker onChange={setCheckIn} value={checkIn} />
        </div>
        <div className="checkout-date">
          <h5>Checkout Date</h5>{" "}
          <DatePicker onChange={setCheckOut} value={checkOut} />
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={onClick}
            >
              Next
            </button>
          </center>
        </div>
      </div>
    </div>
  );
};
export default BookRoom;
