import "./Report.css";
import { useState } from "react";
import Button from 'react-bootstrap/Button';
import axios from "axios";
import { getReportingUrl } from "../getUrl";

import CanvasJSReact from './canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;


const Report = () => {
  const [graph, setGraph] = useState(0);
  const [graphData, setGraphData] = useState({});

  const stats = {
    1: "Hotel Stats",
    2: "Meal Stats",
    3: "Tour Stats",
    4: "Login Stats"
  }

  const statsApi = {
    1: "/hotel-stats",
    2: "/meal-stats",
    3: "/tour-stats",
    4: "/login-stats"
  }

  const exportReport = id => {
    axios.get(getReportingUrl() + statsApi[id]+"-v2")
      .then(response => {
        console.log(response.data);
        const element = document.createElement("a");
        const arr = []
        const file = new Blob([response.data], {
          type: "text/plain"
        });
        element.href = URL.createObjectURL(file);
        element.download = statsApi[id]+".txt";
        document.body.appendChild(element);
        element.click();
      }).catch((err) => {
        console.log(err);
        console.log(err?.response?.data?.message || "Something went wrong")
      })
  }

  const viewGraph = id => {

    axios.get("https://v3xcgr5bike6naytpm4ene6w6e0bzhji.lambda-url.us-east-1.on.aws/" + statsApi[id])
      .then(response => {
        var graphDataPoints = []
        const res = response.data.results
        for (var item in res) {
          graphDataPoints.push({ label: res[item][0]['value'], y: parseInt(res[item][1]['value']) })
        }
        console.log(graphDataPoints)
        const options = {
          title: {
            text: stats[id]
          },
          data: [{
            type: "column",
            dataPoints: graphDataPoints
          }]
        }
        setGraphData(options)
        setGraph(id)
      }).catch((err) => {
        console.log(err?.response?.data?.message || "Something went wrong")
      })
  };

  return (
    <div>
      <div className="statsButton">
      <Button variant="secondary" onClick={() => exportReport(1)}>Export Detailed Hotel Report</Button>&nbsp;
      <Button variant="secondary" onClick={() => exportReport(2)}>Export Detailed Meal Report</Button>&nbsp;
      <Button variant="secondary" onClick={() => exportReport(3)}>Export Detailed Tour Report</Button>&nbsp;
      <Button variant="secondary" onClick={() => exportReport(4)}>Export Detailed Login Report</Button>
      </div>
      
      <div className="statsButton">
      <Button variant="secondary" onClick={() => viewGraph(1)}>Hotel Stats</Button>&nbsp;
      <Button variant="secondary" onClick={() => viewGraph(2)}>Meal Stats</Button>&nbsp;
      <Button variant="secondary" onClick={() => viewGraph(3)}>Tour Stats</Button>&nbsp;
      <Button variant="secondary" onClick={() => viewGraph(4)}>Login Stats</Button>
      </div>
      <br/><br/>
      {graph !== 0 &&
        <>
          <div className="graph">
            <CanvasJSChart options={graphData} />
          </div>
        </>
      }
    </div>
  );
};


export default Report;
