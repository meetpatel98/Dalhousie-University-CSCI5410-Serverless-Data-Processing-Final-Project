import "./BookTour.css";
import { useNavigate, useLocation } from "react-router-dom";
import rentimage from "../../assets/images/Tour.png";
import React, { useState, useEffect } from "react";
import axios from "axios";
import {
    MDBTable,
    MDBTableBody,
    MDBTableHead,
  } from "mdbreact";
import { getTourUrl, getHotelUrl } from "../getUrl";
import { getCustomerIdFromCookie, getAccessTokenFromCookie } from "../getValueFromCookie";


const BookTour = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const booking_id = location.state.booking_id;
  const num_of_days = location.state.num_of_days;
  const [tours, setTours] = useState([]);

  useEffect(() => {
    const data = {
      "num_of_days": num_of_days,
      "customer_id": getCustomerIdFromCookie(),
      "access_token": getAccessTokenFromCookie()
    }
    const header = { 
      'Content-Type': 'application/json'
    }
    axios( {
      method: 'post',
      url: getTourUrl() + '/get_tours',
      headers: header,
      data : data
    })
      .then(response => {
        setTours(response.data)
      }).catch((err) => {
        alert(err?.response?.data?.message || "Something went wrong")
      })
  }, [num_of_days])

  const onClick = (id) => {
    const data = JSON.stringify({
      "customer_id": getCustomerIdFromCookie(), 
      "access_token": getAccessTokenFromCookie(),
      "booking_id": booking_id, 
      "tour_id": id, 
      "quantity": 1
    })
    console.log(data);
    const header = { 
      'Content-Type': 'application/json'
    }
    axios( {
      method: 'post',
      url: getHotelUrl() + '/book_tour',
      headers: header,
      data : data
    })
      .then(response => {
        alert("Booking confirmed");
        navigate("/bookings");
      }).catch((err) => {
        alert(err?.response?.data?.message || "Something went wrong")
      })
    
  };

  return (
    <div className="form-container row">
    <div className="col-md-6">
        <img src={rentimage} width="90%" />
      </div>
      <div className="col-md-6">
        <div className="book-tour">
          <h1>Book Tour</h1>
        </div>
        <div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>Tour Name</th>
                <th>Price</th>
                <th>Num of days</th>
                <th>Itinerary</th>
                <th></th> 
              </tr>
            </MDBTableHead>
            <MDBTableBody>
            {tours && tours.map((tour) => (
              <tr>
                <td>{tour.tour_name}</td>
                <td>${tour.cost}</td>
                <td>{tour.num_of_days}</td>
                <td>{tour.itinerary}</td>
                <td>
                <button
              type="submit"
              className="btn btn-secondary"
              onClick={() => onClick(tour.id)}
            >
              Book
            </button>
                </td>
              </tr>
            ))}
            </MDBTableBody>
          </MDBTable>
        </div>
      </div>
    </div>
  );
};
export default BookTour;
