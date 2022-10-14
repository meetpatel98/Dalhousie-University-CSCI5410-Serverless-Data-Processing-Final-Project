import "./AvailableRooms.css";
import { useLocation, useNavigate } from "react-router-dom";
import React, { useState } from "react";
import {
  MDBTable,
  MDBTableBody,
  MDBTableHead,
} from "mdbreact";
import { getCustomerUrl } from "../getUrl";
import axios from "axios";
import { getCustomerIdFromCookie, getAccessTokenFromCookie } from "../getValueFromCookie";

const AvailabeRooms = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const available_rooms = JSON.parse(location.state.rooms);
  const checkin_date = location.state.checkin_date;
  const checkout_date = location.state.checkout_date;


  const onClick = (room_id) => {
    let data = JSON.stringify({
      "room_id": room_id,
      "customer_id": getCustomerIdFromCookie(),
      "checkin_date": checkin_date,
      "checkout_date": checkout_date,
      "access_token":getAccessTokenFromCookie()
    });

    console.log("data");
    console.log(data);
    let config = {
      method: 'post',
      url: getCustomerUrl()+'/book_room',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    };
    
    axios(config)
    .then(function (response) {
      alert("Request completed");
      console.log(JSON.stringify(response.data));
      navigate("/bookings");
    })
    .catch(function (error) {
      console.log(error);
    });
    
  };

  return (
    <div className="form-container row">
      <div className="col-md-12">
        <div className="available-rooms">
          <h1>Availabe Rooms</h1>
        </div>
        <div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>#</th>
                <th>Amenities</th>
                <th>Bed Type</th>
                <th>Number of Beds</th>
                <th>Cost per night</th>
                <th>Select Your Preference</th> 
              </tr>
            </MDBTableHead>
            <MDBTableBody>
            {available_rooms.map((room) => (
              <tr>
                <td>{room.id}</td>
                <td>{room.amenities.join(', ')}</td>
                <td>{room.bed_type}</td>
                <td>{room.no_of_beds}</td>
                <td>{room.cost_per_day}</td>
                {/* <td className="radio-btn-cell">
                  <input type="radio" value="1" name="room" className="radio-btn" />
                </td> */}
                <td>
                  <button className="btn btn-secondary" onClick={()=>onClick(room.id, )} >
                    Book
                  </button>
                </td>
              </tr>
            ))}

            </MDBTableBody>
          </MDBTable>
        </div>
        {/* <div className="next-btn">
          <center>
          <button
              type="submit"
              className="btn btn-secondary"
              onClick={onClick}
            >
              Book room
            </button>
          </center>
        </div> */}
      </div>
    </div>
  );
};
export default AvailabeRooms;
