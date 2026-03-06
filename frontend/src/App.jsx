import { BrowserRouter, Routes, Route } from "react-router-dom";
import GraphGuardHome from "./home.jsx";
import HowItWorks from "./HowItWorks.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GraphGuardHome />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
      </Routes>
    </BrowserRouter>
  );
}