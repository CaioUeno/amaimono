async function getData(events) {
  try {
    const response = await fetch('http://127.0.0.1:8000/events?names='+events+'&last=10');
    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('There was an error:', error);
  }
}

function plotGraph(response) {

const dat = [];
for (const groupData of response['data']) {
      var trace = {
      x: groupData['x'],
      y: groupData['y'],
      type: 'scatter',  // Required for line charts
      mode: 'lines',    // Can be 'lines', 'markers', or 'lines+markers'
      name: groupData['name']
    };

    dat.push(trace);

 };


    // 2. Define the layout (optional)
    const layout = {
      title: 'Basic Line Chart',
      xaxis: { title: 'X Axis' },
      yaxis: { title: 'Y Axis' }
    };

    // 3. Render the plot in the div with ID 'myDiv'
    Plotly.newPlot('myDiv', dat, layout);

}
resp = getData('INIT,ERROR,SUCCESS').then(response => {plotGraph(response)});

