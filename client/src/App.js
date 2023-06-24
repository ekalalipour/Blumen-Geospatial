
import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {
  const [coordinates, setCoordinates] = useState('');
  const [interpretation, setInterpretation] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleCoordinatesChange = (event) => {
    setCoordinates(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      const coordinatesArray = coordinates
        .split('\n') // Split the input by new line
        .map((line) => line.trim()) // Trim any leading or trailing spaces
        .filter((line) => line !== '') // Remove empty lines
        .map((line) => line.split(',').map(Number)); // Split each line by comma and convert to numbers

      const response = await axios.post('http://blumen-backend:5001/api/overlap', {
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            properties: {},
            geometry: {
              type: 'Polygon',
              coordinates: [coordinatesArray], // Wrap the coordinates in an array
            },
          },
        ],
      });

      const newInterpretation = interpretResponse(response.data);
      console.log('Interpretation:', newInterpretation);
      setInterpretation(newInterpretation);
     
    } catch (error) {
      console.error('Error:', error); // Log the error object to the console
      let errorMessage = 'An error occurred. Please try again.';
      if (error.response && error.response.data && error.response.data.message) {
        if (error.response.data.message === "No overlap found" || error.response.data.message === "AOI size exceeds limit. Please make your AOI smaller.") {
          errorMessage = error.response.data.message;
        }
      } else if (error.message === "AOI size exceeds limit. Please make your AOI smaller.") {
        errorMessage = error.message;
      }
      setErrorMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const interpretResponse = (response) => {
    // // Extract the relevant data from the response
    // const { Des_Tp, FeatClass, Mang_Type } = response;
    // Check if response has the required properties
    if (!response || !response.Des_Tp || !response.FeatClass || !response.Mang_Type) {
      return {
        Des_Tp: [],
        FeatClass: [],
        Mang_Type: [],
      };
    }
    const { Des_Tp = [], FeatClass = [], Mang_Type = [] } = response;

    // Create an object to map the abbreviations to their meanings
    const abbreviationMap = {
      ACC: 'Accuracy',
      CONE: 'Cone',
      FORE: 'Forest',
      FOTH: 'Other',
      HCA: 'Hardwood Components Area',
      LCA: 'Land Cover Area',
      LHCA: 'Large Hardwood Components Area',
      LOTH: 'Other Land',
      LP: 'Land Plan',
      LREC: 'Recreation Area',
      LRMA: 'Rangeland Management Area',
      MIL: 'Military',
      MIT: 'Mitigation',
      NCA: 'National Conservation Area',
      ND: 'National Designation',
      NF: 'National Forest',
      NG: 'National Grassland',
      NLS: 'National Lakeshore',
      NM: 'National Monument',
      NP: 'National Park',
      NRA: 'National Recreation Area',
      NWR: 'National Wildlife Refuge',
      NSBV: 'National Scenic Byway',
      NT: 'National Trail',
      OTHE: 'Other Designation',
      PAGR: 'Private Agricultural',
      PCON: 'Private Conservation',
      PFOR: 'Private Forest',
      PHCA: 'Primary Hardwood Components Area',
      POTH: 'Other Private',
      PPRK: 'Private Park',
      PRAN: 'Private Recreation Area',
      PREC: 'Precision Area',
      PUB: 'Public Land',
      REA: 'Recreation and Entertainment Area',
      REC: 'Recreation Area',
      RECE: 'Recreation Area and Entertainment Area',
      RMA: 'Rangeland Management Area',
      RNA: 'Recreation and National Area',
      SCA: 'State Conservation Area',
      SDA: 'State Designation Area',
      SHCA: 'Small Hardwood Components Area',
      SOTH: 'Other State',
      SP: 'State Park',
      SREC: 'State Recreation Area',
      SRMA: 'State Rangeland Management Area',
      SW: 'State Wilderness',
      TRIBL: 'Tribal Land',
      UNK: 'Unknown',
      WPA: 'Wetland Protection Area',
      WSR: 'Wild and Scenic River',
      TERR: 'Territory',
      TRIB: 'Tribal Land',
    };
  
    // Interpret the Des_Tp data
    const interpretedDes_Tp = Object.entries(Des_Tp).map(([abbreviation, value]) => ({
      abbreviation,
      meaning: abbreviationMap[abbreviation] || 'Unknown',
      value,
    }));
  
    // Interpret the FeatClass data
    const interpretedFeatClass = Object.entries(FeatClass).map(([abbreviation, value]) => ({
      abbreviation,
      meaning: abbreviationMap[abbreviation] || 'Unknown',
      value,
    }));
  
    // Interpret the Mang_Type data
    const interpretedMang_Type = Object.entries(Mang_Type).map(([abbreviation, value]) => ({
      abbreviation,
      meaning: abbreviationMap[abbreviation] || 'Unknown',
      value,
    }));
  
    return {
      Des_Tp: interpretedDes_Tp,
      FeatClass: interpretedFeatClass,
      Mang_Type: interpretedMang_Type,
    };
  };
  

  return (
    <div>
      <h2>Enter Coordinates</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          name="coordinates"
          rows={4}
          onChange={handleCoordinatesChange}
          value={coordinates}
        />

        <button type="submit">Submit</button>
      </form>
      {errorMessage && <p>{errorMessage}</p>}

      {isLoading && <p>Please wait while we process your data. This could take a few minutes...</p>}

      {interpretation.Des_Tp && !isLoading && (
        <div>
          <h2>Interpretation</h2>
          <h3>Des_Tp</h3>
          <ul>
            {interpretation.Des_Tp.filter((item) => item.value !== 0).map((item) => (
              <li key={item.abbreviation}>
                <strong>{item.abbreviation}</strong>: {item.meaning} - {`${(item.value * 100).toFixed(2)}%`}
              </li>
            ))}
          </ul>
          <h3>FeatClass</h3>
          <ul>
            {interpretation.FeatClass.filter((item) => item.value !== 0).map((item) => (
              <li key={item.abbreviation}>
                <strong>{item.abbreviation}</strong>: {item.meaning} - {`${(item.value * 100).toFixed(2)}%`}
              </li>
            ))}
          </ul>
          <h3>Manager_Type</h3>
          <ul>
            {interpretation.Mang_Type.filter((item) => item.value !== 0).map((item) => (
              <li key={item.abbreviation}>
                <strong>{item.abbreviation}</strong>: {item.meaning} - {`${(item.value * 100).toFixed(2)}%`}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Form;





