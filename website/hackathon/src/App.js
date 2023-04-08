import React from 'react';
import BarChart from './BarChart';

const Page = () => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gridTemplateRows: 'repeat(2, 1fr)', height: '100vh' }}>
      {/* First column, first row */}
      <div style={{ backgroundColor: 'red' }}></div>

      {/* Second column, first row */}
      <div style={{ backgroundColor: 'red' }}>
      <BarChart
  data={[
    { label: 'Apples', value: 20 },
    { label: 'Oranges', value: 10 },
    { label: 'Bananas', value: 15 },
    { label: 'Grapes', value: 25 },
    { label: 'Peaches', value: 30 },
    ]}
    width={500}
    height={300}
      />
      </div>

      {/* Third column, first row */}
      <div style={{ backgroundColor: 'red' }}></div>

      {/* First column, second row */}
      <div style={{ backgroundColor: 'red' }}></div>

      {/* Second column, second row */}
      <div style={{ display: 'flex', backgroundColor: 'red' }}>
        {/* Third column, second row */}
        <div style={{ flex: 1, backgroundColor: 'red' }}></div>
        <div style={{ flex: 1, backgroundColor: 'red' }}></div>
      </div>
    </div>
  );
};

export default Page;
