import "./ThirdFactorAuth.css";
import rentimage from "../../assets/images/HomeGlobeIcon.png";
import { useState } from "react";
import { Formik, Form } from "formik";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useCookies } from "react-cookie";

function generateText() {
  var text = "";
  var allowedCharacters = "abcdefghijklmnopqrstuvwxyz";

  for (var i = 0; i < 6; i++)
    text += allowedCharacters.charAt(
      Math.floor(Math.random() * allowedCharacters.length)
    );

  return text;
}

const TEXT = generateText();

const ThirdFactorAuth = () => {
  const [decodedText, setDecodedText] = useState(defaultValues);
  const [cookies, setCookies] = useCookies(["State","loginTimestamp","Customer_Id"]);
  // const [cookie, setCookie] = useCookies(["loginTimestamp"]);
  
  const navigate = useNavigate();
  const signupForm = (formValues) => {
    console.log("form values are " + formValues);

    axios
      .post(
        "https://us-central1-serverless-a4-355004.cloudfunctions.net/caesarCipherAuth",
        {
          text: TEXT,
          decoded: decodedText,
          customerId: cookies.Customer_Id
        }
      )
      .then((res) => {
        console.log(res)
        setCookies("State",  res.data.state)
        if(res.data.state == false){
          alert("Cipher Mismatched")
        }
        else{
          setCookies("loginTimestamp", Number(Date.now()));
          navigate("/bookroom");
        }

  
      })
      .catch((error) => {
        console.log(error);
        alert(error);
      });
  };
  return (
    <Formik
      initialValues={defaultValues}
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
                <h3>Third Factor Authentication</h3>
                <div className="mb-2">
                  <label>Cipher String</label>
                  <input
                    type="text"
                    className="form-control"
                    name="cipher-string"
                    id="cipher-string"
                    value={TEXT}
                    disabled
                  />
                </div>
                <div className="mb-2">
                  <label>Decoded Text</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter decoded text"
                    name="decodedText"
                    id="decodedText"
                    value={decodedText.decoded}
                    onBlur={handleBlur}
                    onChange={(e) => setDecodedText(e.target.value)}
                  />
                </div>
                <div className="d-grid pt-2">
                  <center>
                    <button
                      type="submit"
                      className="btn btn-secondary"
                    >
                      Sign In
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
  decoded: "",
};

export default ThirdFactorAuth;
