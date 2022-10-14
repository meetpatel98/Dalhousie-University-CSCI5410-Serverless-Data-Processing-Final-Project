import "./AdminFeedback.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import {
    MDBTable,
    MDBTableBody,
    MDBTableHead,
  } from "mdbreact";
import { getHotelUrl } from "../getUrl";


const Feedback = () => {

  const [feedbacks, setFeedbacks] = useState([]);

  useEffect(() => {

    const header = { 
      'Content-Type': 'application/json'
    }
    axios( {
      method: 'get',
      url: getHotelUrl() + '/get_feedbacks',
      headers: header
    })
      .then(response => {
        setFeedbacks(response.data)
      }).catch((err) => {
        alert(err?.response?.data?.message || "Something went wrong")
      })
  }, [])


  return (
    <div className="form-container row">
      <div className="col-md-12">
        <div className="book-tour">
          <h1>Feedbacks</h1>
        </div>
        <div>
          <MDBTable striped>
            <MDBTableHead>
              <tr>
                <th>Booking Id</th>
                <th>Feedback</th>
                <th>Polarity</th>
                <th>Sentiment Score</th>
               
              </tr>
            </MDBTableHead>
            <MDBTableBody>
            {feedbacks && feedbacks.map((feedback) => (
              <tr>
                <td>{feedback.booking_id}</td>
                <td>{feedback.feedback}</td>
                <td>{feedback.feedback_polarity}</td>
                <td>{feedback.feedback_sentimentscore}</td>
                <td>
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
export default Feedback;
