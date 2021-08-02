
Highcharts.chart('chart1', {
    chart: {
    backgroundColor:'#0000',
    height: 250,
    animation: false,
    type: 'area',
    zoomType: 'xy'
    },
    
    navigation: {
buttonOptions: {
  enabled: false
  }
 },

        title: {
        text: 'RSSI Value',
        style: {
                color: '#e6ffff',
                fontSize: '22px'
            
            }
    },

    xAxis: [{

        categories: x_axis_data,
        crosshair: true
    },],
    yAxis: { // Primary yAxis
        max:0,
        min:-120,
        startOnTick: false,
    gridLineWidth: 0,
    labels: {
        gridLineWidth:0,
            format: '{value}',
            style: {
                color: '#ffffff'
            }
        },
        title: {
            text: 'RSSI Value',
            style: {
                color: '#ffffff'
            }
        }
    },
    tooltip: {
        pointFormat: '{series.name}  <b>{point.y:,.0f}</b><br/>'
    },
    plotOptions: {
    series: {
    animation: false,
        zones: [{
            color: '#00ff72'

        }]
    }


    },
       legend: {
        
      itemStyle:{color: '#e6ffff'},
        
        
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || // theme
            'transparent'
    },
    series: [ 

    {
        color: '#00ff72',
        name: 'RSSI value',

    data: area_graph_y_axis
    }]
});