import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Signup from "./components/UserManagement/Signup";
import Signin from "./components/UserManagement/Signin";
import SecondFactorAuth from './components/UserManagement/SecondFactorAuth';
import ThirdFactorAuth from './components/UserManagement/ThirdFactorAuth';
import BookRoom from './components/MessagePassingModule/BookRoom';
import AvailabeRooms from './components/MessagePassingModule/AvailableRooms';
import Bookings from './components/MessagePassingModule/Bookings';
import OrderMeal from './components/MessagePassingModule/OrderMeal';
import BookTour from './components/MessagePassingModule/BookTour';
import Notifications from './components/MessagePassingModule/Notifications';
import Feedback from './components/MessagePassingModule/Feedback';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import Report from './components/Report/Report';
import Visualization from './components/OtherEssentialModules/Visualization';
import AdminFeedback from './components/OtherEssentialModules/AdminFeedback';
import AdminLogin from './components/Admin/AdminLogin';
import HomePage from './components/Home/home';

function App() {
  return (
    <div >
     <BrowserRouter>
     <Header/>
       <Routes>
      <Route path='/' element={<HomePage/>}></Route>
       <Route path="/signup" element={<Signup />}></Route>
       <Route path="/signin" element={<Signin />}></Route>
       <Route path="/secondfactorauthication" element={<SecondFactorAuth />}></Route>
       <Route path="/thirdfactorauth" element={<ThirdFactorAuth />}></Route>
       <Route path="/bookroom" element={<BookRoom />}></Route>
       <Route path="/availablerooms" element={<AvailabeRooms />}></Route>
       <Route path="/bookings" element={<Bookings />}></Route>
       <Route path="/ordermeal" element={<OrderMeal />}></Route>
       <Route path="/booktour" element={<BookTour />}></Route>
       <Route path="/notifications" element={<Notifications />}></Route>
       <Route path="/feedback" element={<Feedback />}></Route>
       <Route path="/report" element={<Report />}></Route>
       <Route path='/visualization' element={<Visualization/>}></Route>
       <Route path='/adminfeedback' element={<AdminFeedback/>}></Route>
       <Route path='/admin' element={<AdminLogin/>}></Route>
       </Routes>
       <Footer/>
     </BrowserRouter>
    </div>
  );
}

export default App;
