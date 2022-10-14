import "./Bookings.css";
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  MDBTable,
  MDBTableBody,
  MDBTableHead,
  MDBInput,
  MDBContainer,
  Radio,
} from "mdbreact";
import { getHotelUrl, getMealUrl, getTourUrl } from "../getUrl";
import { getCustomerIdFromCookie, getAccessTokenFromCookie } from "../getValueFromCookie";

const Bookings = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [meals, setMeals] = useState([]);
  const [tours, setTours] = useState([]);


  useEffect(() => {
    const data = {
      "customer_id": getCustomerIdFromCookie(),
      "access_token": getAccessTokenFromCookie()
    }
    const header = { 
      'Content-Type': 'application/json'
    }
    axios( {
      method: 'post',
      url: getHotelUrl() + '/get_booking_details',
      headers: header,
      data : data
    })
      .then(response => {
        setBookings(response.data)
      }).catch((err) => {
        alert(err?.response?.data?.message || "Something went wrong")
      })
      axios( {
        method: 'post',
        url: getMealUrl() + '/get_meal_bookings',
        headers: header,
        data: data 
      })
        .then(response => {
          setMeals(response.data)
        }).catch((err) => {
          alert(err?.response?.data?.message || "Something went wrong")
        })
        axios( {
          method: 'post',
          url: getTourUrl() + '/get_tour_bookings',
          headers: header,
          data : data
        })
          .then(response => {
            setTours(response.data)
          }).catch((err) => {
            alert(err?.response?.data?.message || "Something went wrong")
          })
  }, [])

  const orderMeal = (booking_id) => {
    navigate("/ordermeal", {"state":{"booking_id" : booking_id}});
  };

  const bookTour = (booking) => {
    const date1 = new Date(booking.checkin_date);
    const date2 = new Date(booking.checkout_date);
    const num_of_days = Math.abs(date2 - date1)/ (1000 * 60 * 60 * 24)
    navigate("/booktour", {'state':{"booking_id": booking.id, "num_of_days": num_of_days}});
  };

  const provideFeedback = (id) => {
    navigate("/feedback", {'state':{"booking_id": id}});
  };

  const notifications = () => {
    navigate("/notifications");
  };

  return (
    <div className="form-container row">
      <div className="col-md-12">
        <div className="bookings">
          <h1>Bookings</h1>
          <button
            type="submit"
            className="btn-notifications btn-secondary"
            onClick={notifications}
          >
            Notifications
          </button>
        </div>
        <div>
          <div className="hotel-bookings">
            <h1>Booked Rooms</h1>
          </div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>#</th>
                <th>Timestamp</th>
                <th>Check-in date</th>
                <th>Check-out date</th>
                <th>Total Cost</th>
                <th>Select Your Preference</th>
              </tr>
            </MDBTableHead>
            <MDBTableBody>
              {bookings.map((booking) => (
              <tr>
                <td>{booking.id}</td>
                <td>{booking.timestamp}</td>
                <td>{booking.checkin_date}</td>
                <td>{booking.checkout_date}</td>
                <td>${booking.total_cost}</td>
                <td>
                  <button
                    type="submit"
                    className="btn-table btn-secondary"
                    onClick={() => orderMeal(booking.id)}
                  >
                    Order Meal
                  </button>
                  <button
                    type="submit"
                    className="btn-table btn-secondary"
                    onClick={() => bookTour(booking)}
                  >
                    Book Tour
                  </button>
                  <button
                    type="submit"
                    className="btn-table btn-secondary"
                    onClick={() => provideFeedback(booking.id)}
                  >
                    Provide Feedback
                  </button>
                </td>
              </tr>
            ))}
            </MDBTableBody>
          </MDBTable>
        </div>
        <div>
          <div className="ordered-meals">
            <h1>Ordered Meals</h1>
          </div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>#</th>
                <th>Timestamp</th>
                <th>Meal Name</th>
                <th>Quantity</th>
                <th>Total Cost</th>
              </tr>
            </MDBTableHead>
            <MDBTableBody>
            {meals && meals.map((meal) => (
              <tr>
                <td>{meal.booking_id}</td>
                <td>{meal.timestamp}</td>
                <td>{meal.meal_name}</td>
                <td>{meal.quantity}</td>
                <td>${meal.total_cost}</td>
              </tr>
            ))}
            </MDBTableBody>
          </MDBTable>
        </div>
        <div>
          <div className="booked-tours">
            <h1>Booked Tours</h1>
          </div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>#</th>
                <th>Timestamp</th>
                <th>Tour Name</th>
                <th>Num of days</th>
                <th>Quantity</th>
                <th>Total Cost</th>
              </tr>
            </MDBTableHead>
            <MDBTableBody>
            {tours && tours.map((tour) => (
              <tr>
                <td>{tour.booking_id}</td>
                <td>{tour.time_stamp}</td>
                <td>{tour.tour_name}</td>
                <td>{tour.num_of_days}</td>
                <td>{tour.quantity}</td>
                <td>${tour.total_cost}</td>
              </tr>
            ))}
            </MDBTableBody>
          </MDBTable>
        </div>
      </div>
    </div>
  );
};
export default Bookings;
