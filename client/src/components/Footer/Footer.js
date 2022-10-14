import "./Footer.css";
import { Navbar, Nav } from "react-bootstrap";

const Footer = () => {
  return (
    <div>
      <iframe width="600" className='chatbot' height="450" src="https://d10wp5iuzpvsrx.cloudfront.net/index.html" title="Help!"></iframe>
    <Navbar
      className="bg-dark navbar-dark footer"
      collapseOnSelect
      expand="md"
      bg="light"
      sticky="bottom"
    >
      <div className="container-fluid" id="navbar">
          <Nav>
            <Nav.Link href="/signin" active>
              Home
            </Nav.Link>
          </Nav>
      </div>
    </Navbar>
    </div>
  );
};

export default Footer;
