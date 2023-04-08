import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const BarChart = ({ data, width, height }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);

    // Define margins and dimensions
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    // Create scales
    const x = d3
      .scaleBand()
      .range([0, chartWidth])
      .padding(0.1)
      .domain(data.map(d => d.label));

    const y = d3
      .scaleLinear()
      .range([chartHeight, 0])
      .domain([0, d3.max(data, d => d.value)]);

    // Create axes
    const xAxis = d3.axisBottom(x);

    const yAxis = d3.axisLeft(y).ticks(5);

    svg
      .select('.x-axis')
      .attr('transform', `translate(0, ${chartHeight})`)
      .call(xAxis);

    svg.select('.y-axis').call(yAxis);

    // Create bars
    svg
      .selectAll('.bar')
      .data(data)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.label))
      .attr('y', d => y(d.value))
      .attr('width', x.bandwidth())
      .attr('height', d => chartHeight - y(d.value));
  }, [data, height, width]);

  return (
    <svg ref={svgRef} width={width} height={height}>
      <g className="x-axis" />
      <g className="y-axis" />
    </svg>
  );
};

export default BarChart;
