import "./Header.css";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Header = (props) => {
  const [cookie, setCookie, removeCookie] = useCookies([
    "Email",
    "AccessToken",
    "Customer_Id",
    "State",
    "loginTimestamp",
    "Admin"
  ]);

  let navigate = useNavigate();
  const isState = cookie.State;
  const isAdmin = cookie.Admin;
  console.log(cookie.Email);
  const LogOut = () => {
    axios
      .post(
        "https://us-central1-serverless-a4-355004.cloudfunctions.net/userLogs",
        {
          customerId: cookie.Customer_Id,
          email: cookie.Email,
          loginTimestamp: cookie.loginTimestamp,
          logoutTimestamp: Number(Date.now()),
        }
      )
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
        alert(error);
      });

    removeCookie("Email");
    removeCookie("AccessToken");
    removeCookie("Customer_Id");
    removeCookie("State");
    removeCookie("loginTimestamp");
    removeCookie("Admin");
    navigate();
  };

  return (
    <nav class="navbar navbar-expand navbar-dark bg-dark sticky-top">
      <ul class="navbar-nav">
      <li class="nav-item active">
          <a class="nav-link active" href="/">
            Home
          </a>
        </li>
        { isAdmin ? (<></>) : (
        <li class="nav-item active">
          <a class="nav-link active" href="/admin">
            Admin
          </a>
        </li>
        )}
      </ul>
      {(isState || isAdmin )? (
        <ul class="navbar-nav" style={{ marginLeft: "auto" }}>
          <li class="nav-item  active">
            <a class="nav-link" onClick={LogOut} href="/signin">
              Signout
            </a>
          </li>
        </ul>
      ) : (
        <>
          <ul class="navbar-nav" style={{ marginLeft: "auto" }}>
            <li class="nav-item active">
              <a class="nav-link" href="/signin">
                Login
              </a>
            </li>
            <li class="nav-item  active">
              <a class="nav-link" href="/">
                Signup
              </a>
            </li>
          </ul>
        </>
      )}
    </nav>
  );
};

export default Header;
