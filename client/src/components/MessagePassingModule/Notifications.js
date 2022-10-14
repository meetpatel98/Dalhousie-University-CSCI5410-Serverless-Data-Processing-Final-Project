import "./Notifications.css";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import { getCustomerIdFromCookie } from "../getValueFromCookie";
import { getNotificationUrl } from "../getUrl";
import {
    MDBTable,
    MDBTableBody,
    MDBTableHead,
  } from "mdbreact";
import axios from "axios";

const Notifications = () => {
  const navigate = useNavigate();
  const [msgs, setMsgs] = useState([])

  useEffect(() => {
    let data = JSON.stringify({
      "customer_id": getCustomerIdFromCookie()
    });
    
    let config = {
      method: 'post',
      url: getNotificationUrl()+'/pullNotification',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    };
    
    axios(config)
    .then(function (response) {
      let array = response.data;
      array.sort(function (a, b) {
        let dateA = new Date(a.timestamp), dateB = new Date(b.timestamp)
        return dateB - dateA 
      });
      setMsgs(array);
      console.log(array);
    })
    .catch(function (error) {
      console.log(error);
    });
  }, [])

  const back = () => {
    navigate("/bookings");
  };

  return (
    <div className="form-container row">
      <div className="col-md-12">
        <div className="notifications">
          <h1>Notifications</h1>
          {/* <button
              type="submit"
              className="btn btn-secondary"
              onClick={getMessages}
            >
              Click to pull new notifications
            </button> */}
        </div>
        <div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>Timestamp</th>
                <th>Messages</th>
              </tr>
            </MDBTableHead>
            <MDBTableBody>
              {msgs.map((msg) => (
                  <tr>
                    <td>{msg.timestamp}</td>
                    <td>{msg.message}</td>
                  </tr>
                ))}
            </MDBTableBody>
          </MDBTable>
        </div>
        <div className="submit-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={back}
            >
              Back
            </button>
            
          </center>
        </div>
      </div>
    </div>
  );
};
export default Notifications;
