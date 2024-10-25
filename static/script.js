// function updateMargin() {
//     const margin = document.getElementById('margin').value;
//     $.ajax({
//         url: '/update_margin',
//         type: 'POST',
//         contentType: 'application/json',
//         data: JSON.stringify({ margin: parseInt(margin) }),
//         success: function(response) {
//             alert('Margin updated to ' + response.margin);
//         }
//     });
// }

// function stopProcessing() {
//     $.ajax({
//         url: '/stop',
//         type: 'POST',
//         success: function(response) {
//             alert('Processing stopped.');
//         }
//     });
// }
