import "./Signup.css";
import rentimage from "../../assets/images/HomeGlobeIcon.png";
import { Link } from "react-router-dom";
import { useState } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { max } from "date-fns";

const Signup = () => {
  const [userDetails, setUserDetails] = useState(defaultValues);
  const navigate = useNavigate();
  // const [Question, setQuestion] = useState();
  const signupForm = (formValues) => {
    setUserDetails(formValues);

    axios
      .post(
        "https://us-central1-serverless-a4-355004.cloudfunctions.net/signup",
        {
          ...formValues,
        }
      )
      .then((res) => {
        alert(res.data.message)
        console.log(res);
        navigate("/signin");
      })
      .catch((error) => {
        alert(error);
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
                <h3>Sign Up</h3>
                <div className="mb-2">
                  <label>Name</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Name"
                    name="name"
                    id="name"
                    value={values.name}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.name && touched.name ? (
                    <span className="error-feedback">{errors.name}</span>
                  ) : null}
                </div>
                <div className="mb-2">
                  <label>Email address</label>
                  <input
                    type="email"
                    className="form-control"
                    placeholder="Enter email"
                    name="email"
                    id="email"
                    value={values.email}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.email && touched.email ? (
                    <span className="error-feedback">{errors.email}</span>
                  ) : null}
                </div>
                <div className="mb-2">
                  <label>Password</label>
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Enter password"
                    name="password"
                    id="password"
                    value={values.password}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.password && touched.password ? (
                    <span className="error-feedback">{errors.password}</span>
                  ) : null}
                </div>
                <div className="mb-2">
                  <label>Security Question</label>
                  <div>
                    <select
                      id="question"
                      onChange={handleChange}
                    >
                      <option>Please select a question</option>
                      <option value="What’s your favorite movie?">
                        What’s your favorite movie?
                      </option>
                      <option value="What was your first car?">
                        What was your first car?
                      </option>
                      <option value="What is your Year of birth?">
                        What is your Year of birth?
                      </option>
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
                <div className="mb-2">
                  <label>Secret Key</label>
                  <input
                    type="Number"
                    className="form-control"
                    placeholder="Enter Secret Key"
                    name="key"
                    id="key"
                    value={values.key}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                   {errors.key && touched.key ? (
                    <span className="error-feedback">{errors.key}</span>
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
                <p className="existing-user text-left">
                  <center>
                    Already a user? <Link to="/signin">sign in</Link>
                  </center>
                </p>
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
  name: "",
  email: "",
  password: "",
  question: "",
  answer: "",
  key:"",
};

const SignupFormValidation = Yup.object().shape({
  name: Yup.string().required("First name is required"),

  answer: Yup.string().required("Answer is required"),

  email: Yup.string().email("Invalid Email").required("Email is required"),

  password: Yup.string()
    .required("Password is required")
    .min(8, "Password length should be 8 chars minimum")
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
      "Password should contains at least one uppercase letter, one lowercase letter, one number and special character"
    ),

    key: Yup.number().required("Secret Key is required").min(0).max(6)
});

export default Signup;
