import "./AdminLogin.css";
import rentimage from "../../assets/images/HomeGlobeIcon.png";
import { useState } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCookies } from "react-cookie";

const AdminLogin = () => {
  const [adminDetails, setAdminDetails] = useState(defaultValues);
  const [cookie, setCookie, removeCookie] = useCookies([
    "Email",
    "AccessToken",
    "Customer_Id",
    "State",
    "loginTimestamp",
  ]);

  const navigate = useNavigate();
  const signinForm = (formValues) => {
    setAdminDetails(formValues);
    axios
      .post(
        "https://us-central1-serverless-a4-355004.cloudfunctions.net/adminlogin",
        {
          ...formValues,
        }
      )
      .then((res) => {
        console.log(res);
        setCookie("Admin", true);
        removeCookie("Email");
        removeCookie("AccessToken");
        removeCookie("Customer_Id");
        removeCookie("State");
        removeCookie("loginTimestamp");
        navigate("/visualization");
      })
      .catch((error) => {
        console.log(error);
        alert("Invalid Credentials.")
      });
  };

  return (
    //Formik is a library used for form validation  https://formik.org/
    <Formik
      initialValues={defaultValues}
      validationSchema={SigninFormValidation}
      onSubmit={signinForm}
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
                <h3>Admin Sign In</h3>
                <div className="mb-3">
                  <label>Username</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter Username"
                    name="username"
                    id="username"
                    value={values.username}
                    onBlur={handleBlur}
                    onChange={handleChange}
                  />
                  {errors.username && touched.username ? (
                    <span className="error-feedback">{errors.username}</span>
                  ) : null}
                </div>

                <div className="mb-3">
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
                </div>

                <div className="d-grid">
                  <center>
                    <button
                      type="submit"
                      className="btn btn-secondary"
                      disabled={!(dirty && isValid)}
                    >
                      Login
                    </button>
                  </center>
                </div>
              </Form>
            </div>

            {/* rent image has been taken from the "https://www.freepik.com/free-vector/renting-electronic-device-renting-electronics-website-new-device-rent-terms-use-conditions-gadget-rental-test-equipment-lease_13450501.htm#query=equipment%20rental&position=12&from_view=search" */}
            <div className="col-md-6">
              <img src={rentimage} width="90%" />
            </div>
          </div>
        );
      }}
    </Formik>
  );
};

const SigninFormValidation = Yup.object().shape({
  username: Yup.string().required("Username is required"),

  password: Yup.string().required("Password is required"),
});

const defaultValues = {
  username: "",
  password: "",
};

export default AdminLogin;
