import "./Feedback.css";
import feedback from "../../assets/images/Feedback.png";
import { useState } from "react";
import { Formik, Form } from "formik";
import axios from "axios";
import * as Yup from "yup";
import { useNavigate, useLocation } from "react-router-dom";
import { getHotelUrl } from "../getUrl";
import { getCustomerIdFromCookie, getAccessTokenFromCookie } from "../getValueFromCookie";

const Feedback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const booking_id = location.state.booking_id

  const signupForm = (formValues) => {
    const data = {
      "customer_id": getCustomerIdFromCookie(), 
      "access_token": getAccessTokenFromCookie(),
      "booking_id": booking_id, 
      "feedback": formValues.feedback
    }
    const header = { 
      'Content-Type': 'application/json'
    }
    axios( {
      method: 'post',
      url: getHotelUrl() + '/post_hotel_feedback',
      headers: header,
      data : data
    })
      .then(response => {
        navigate("/bookings");
      }).catch((err) => {
        alert(err?.response?.data?.message || "Something went wrong")
      })
    
  };
  return (
    <Formik
      initialValues={defaultValues}
      validationSchema={SignupFormValidation}
      onSubmit={signupForm}
    >
      {(formik) => {
        const {
          values,
          errors,
          touched,
          isValid,
          dirty,
          handleChange,
          handleSubmit,
          handleBlur,
        } = formik;

        return (
          <div className="form-container row">
            <div className="col-md-6 form">
              <Form onSubmit={handleSubmit}>
                <div className="feedback">
                <h3>Feedback</h3>
                </div>
                <div className="mb-2">
                  <textarea
                    type="text"
                    className="form-control"
                    placeholder="Provide Feedback"
                    name="feedback"
                    id="feedback"
                    value={values.feedback}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.feedback && touched.feedback ? (
                    <span className="error-feedback">{errors.feedback}</span>
                  ) : null}
                </div>
                <div className="d-grid pt-2">
                  <center>
                    <button
                      type="submit"
                      className="btn btn-secondary"
                      disabled={!(dirty && isValid)}
                    >
                      Submit
                    </button>
                  </center>
                </div>
              </Form>
            </div>
            <div className="col-md-6">
              <img src={feedback} width="90%" />
            </div>
          </div>
        );
      }}
    </Formik>
  );
};

const defaultValues = {
    feedback: "",
};

const SignupFormValidation = Yup.object().shape({

    feedback: Yup.string().required("Feedback is required"),

});


export default Feedback;
