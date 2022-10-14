import "./SecondFactorAuth.css";
import rentimage from "../../assets/images/HomeGlobeIcon.png";
import { useState } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { useCookies } from "react-cookie";


const SecondFactorAuth = () => {
  const [requestData, setRequestData] = useState(defaultValues)
  const [cookies, setCookies] = useCookies(["Email", "Customer_Id"]);
  const navigate = useNavigate();
  const signupForm = (formValues) => {
    formValues["email"]=cookies.Email
    setRequestData(formValues)
    axios
      .post(
        "https://us-central1-serverless-a4-355004.cloudfunctions.net/questionAnsAuth",
        {
          ...formValues,
        }
      )
      .then((res) => {
        console.log(res.data.id);
        setCookies("Customer_Id", res.data.id)
        navigate("/thirdfactorauth");

      })
      .catch((error) => {
        console.log(error.response.data.message)
        alert(error.response.data.message);
      });

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
                <h3>Second Factor Authentication</h3>
                <div className="mb-2">
                  <label>Security Question</label>
                  <div>
                    <select
                      id="question"
                      // value={Question}
                      onChange={handleChange}
                    >
                      <option>Please select a question</option>
                      <option value="What’s your favorite movie?">What’s your favorite movie?</option>
                      <option value="What was your first car?">What was your first car?</option>
                      <option value="What is your Year of birth?">What is your Year of birth?</option>
                    </select>
                  </div>
                </div>
                <div className="mb-2">
                  <label>Answer</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter Answer"
                    name="answer"
                    id="answer"
                    value={values.answer}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.answer && touched.answer ? (
                    <span className="error-feedback">{errors.answer}</span>
                  ) : null}
                </div>
                <div className="d-grid pt-2">
                  <center>
                    <button
                      type="submit"
                      className="btn btn-secondary"
                      disabled={!(dirty && isValid)}
                    >
                      Next
                    </button>
                  </center>
                </div>
              </Form>
            </div>
            <div className="col-md-6">
              <img src={rentimage} width="90%" />
            </div>
          </div>
        );
      }}
    </Formik>
  );
};

const defaultValues = {
  question: "",
  answer: "",
  email:""
};

const SignupFormValidation = Yup.object().shape({
  answer: Yup.string().required("Answer is required"),

});

export default SecondFactorAuth;
