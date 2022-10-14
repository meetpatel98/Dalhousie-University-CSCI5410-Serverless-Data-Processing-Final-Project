import "./home.css";
import { useLocation, useNavigate } from "react-router-dom";
import rentimage from "../../assets/images/Welcome.png";
import React, { useEffect, useState } from "react";
import { getMealUrl, getHotelUrl } from "../getUrl";
import { getAccessTokenFromCookie, getCustomerIdFromCookie } from "../getValueFromCookie";

const HomePage = () => {

    const navigate = useNavigate();

    const handleClick = () => {

        let id = getCustomerIdFromCookie();
        if (id !== undefined && id != null && id !== ''){
                navigate("/bookroom");
        } else {
                navigate("/signin")
        }
        }
    

  return (
    <div className="form-container row">
      <div className="col-md-7">
        <div className="order-meal">
               <h1>Click <a onClick={handleClick} className="here">here</a> to get started</h1>
        </div>
        <div>
          
        </div>
      </div>
      <div className="col-md-5">
        <img src={rentimage} width="90%" />
      </div>
    </div>
  );
};
export default HomePage;
