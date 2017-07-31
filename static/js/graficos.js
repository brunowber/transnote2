

window.onload = function () {
  altura = $('.agentesNaoSincronizados').height()
  $('.graficoInfracoes').height(altura)
  $('.canvasjs-chart-credit').hide()
  alturaGrafico=altura-(altura/100)
  $('.canvasjs-chart-canvas').height(alturaGrafico)
  var chart = new CanvasJS.Chart("grafico", {
    theme: "theme1",//theme1
    title:{
      text: ''              
    },
    data: [              
      {
      // Change type to "bar", "splineArea", "area", "spline", "pie",etc.
      type: "line",
      dataPoints: [
        { label: "13", y: 10 },
        { label: "14", y: 15 },
        { label: "15", y: 25 },
        { label: "16", y: 30 },
        { label: "17", y: 28 },
        { label: "18", y: 40 }
        ]
      }
    ]
  });

  chart.render();
  $('.canvasjs-chart-canvas').height(alturaGrafico)
}
