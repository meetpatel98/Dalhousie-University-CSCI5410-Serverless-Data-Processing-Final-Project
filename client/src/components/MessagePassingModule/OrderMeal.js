import "./OrderMeal.css";
import { useLocation, useNavigate } from "react-router-dom";
import rentimage from "../../assets/images/OrderMeal.png";
import React, { useEffect, useState } from "react";
import { getMealUrl, getHotelUrl } from "../getUrl";
import { getAccessTokenFromCookie, getCustomerIdFromCookie } from "../getValueFromCookie";
import {
    MDBTable,
    MDBTableBody,
    MDBTableHead,
  } from "mdbreact";
import axios from "axios";

const OrderMeal = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const booking_id = location.state.booking_id;
  const [meals, setMeals] = useState([]);
  useEffect(() => {
    let data = '';

    let config = {
      method: 'get',
      url: getMealUrl()+'/get_meals',
      headers: { },
      data : data
    };

    axios(config)
    .then(function (response) {
      console.log(JSON.stringify(response.data));
      setMeals(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
  }, [])
  const onClick = (meal_id) => {

    let data = JSON.stringify({
      "meal_id": meal_id,
      "customer_id": getCustomerIdFromCookie(),
      "booking_id": booking_id,
      "quantity": 1,
      "access_token":getAccessTokenFromCookie()
    });
    console.log("---data---");
    console.log(data);
    
    let config = {
      method: 'post',
      url: getHotelUrl()+'/order_meal',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    };
    
    axios(config)
    .then(function (response) {
      alert("Meal order request placed successfully");
      console.log(JSON.stringify(response.data));
      navigate("/bookings");
    })
    .catch(function (error) {
      console.log(error);
    });

    
  };

  return (
    <div className="form-container row">
      <div className="col-md-7">
        <div className="order-meal">
          <h1>Order Meal</h1>
        </div>
        <div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
              <th>#</th>
                <th>Meal Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Select Your Preference</th> 
              </tr>
            </MDBTableHead>
            <MDBTableBody>
              {meals.map((meal) => (
                <tr>
                  <td>{meal.id}</td>
                  <td>{meal.name}</td>
                  <td>{meal.description}</td>
                  <td>{meal.cost}</td>
                  {/* <td className="radio-btn-cell">
                    <input type="radio" value="1" name="room" className="radio-btn" />
                  </td> */}
                  <td>
                    <button className="btn btn-secondary" onClick={()=>onClick(meal.id)} >
                      Order
                    </button>
                  </td>
                </tr>
              ))}
            </MDBTableBody>
          </MDBTable>
        </div>
        {/* <div className="submit-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={onClick}>
              Order
            </button>
          </center>
        </div> */}
      </div>
      <div className="col-md-5">
        <img src={rentimage} width="90%" />
      </div>
    </div>
  );
};
export default OrderMeal;
