import "./Visualization.css";
import { useNavigate } from "react-router-dom";
import rentimage from "../../assets/images/graphs.jpg";
import React from "react";
import axios from "axios";

const Visualization = () => {

  const navigate = useNavigate();
  const spendingGraph = () => {
    axios.get(
      "https://us-central1-b00896765a4partb.cloudfunctions.net/booking_details"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/meal_order"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/meal"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/tour_booking"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/tour_booking"
    );

    window.open(
      "https://datastudio.google.com/embed/reporting/129fe67d-e227-4710-891c-166f2b3bca32/page/ACXyC"
    );
  };

  // const reportGeneration = () => {
  //   window.open(
  //     "https://datastudio.google.com/embed/reporting/111d0138-0319-4d47-8661-d198f0faac1d/page/tEnnC"
  //   );
  // };

  const feedbackReport = () => {
    navigate("/adminfeedback")
  };

  const accessReport = () => {
    navigate("/report")
  };

  const foodOrderGraph = () => {
    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/meal_order"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/meal"
    );

    window.open(
      "https://datastudio.google.com/embed/reporting/3d730b90-2684-4dab-9915-df1629f6e4b8/page/6LXyC"
    );
  };

  const tourBookingGraph = () => {
    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/tour_booking"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/tour"
    );

    window.open(
      "https://datastudio.google.com/embed/reporting/ac264ff7-a113-443c-8d6a-c0457b56c958/page/VMXyC"
    );
  };


  const bookingGraph = () => {
    axios.get(
      "https://us-central1-b00896765a4partb.cloudfunctions.net/booking_details"
    );

    axios.get(
      "https://us-east1-b00896765a4partb.cloudfunctions.net/room"
    );

    window.open(
      "https://datastudio.google.com/embed/reporting/2edc3483-6569-4661-abb0-d84e1036a5df/page/gLXyC"
    );
  };


  return (
    <div className="form-container row">
      <div className="col-md-6">
        <img src={rentimage} width="90%" />
      </div>
      <div className="col-md-6">
        <div className="visualization">
          <h3>Visualization</h3>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={bookingGraph}
            >
              Customer Room Booking Graph
            </button>
          </center>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={foodOrderGraph}
            >
              Customer Food Orders Graph
            </button>
          </center>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={tourBookingGraph}
            >
              Customer Tour Booking Graph
            </button>
          </center>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={spendingGraph}
            >
              Customer Spendings Graph
            </button>
          </center>
        </div>
        <div className="report">
          <h3>Report</h3>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={accessReport}
            >
              Access Reports
            </button>
          </center>
        </div>
        <div className="next-btn">
          <center>
            <button
              type="submit"
              className="btn btn-secondary"
              onClick={feedbackReport}
            >
              Feedback Report
            </button>
          </center>
        </div>
      </div>
    </div>
  );
};
export default Visualization;
