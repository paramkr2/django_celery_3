// custom javascript

$(document).ready(() => {
  console.log('Sanity Check!');
});

$('.button').on('click', function() {
  $.ajax({
    url: '/trigger_report/',
    data: { type: $(this).data('type') },
    method: 'POST',
  })
  .done((res) => {
    getStatus(res.task_id);
  })
  .fail((err) => {
    console.log(err);
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/get_report/${taskID}/`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.task_id}</td>
        <td>${res.task_status}</td>
        <td>  <a href="${res.task_result}">${res.task_result}</a>$</td>
      </tr>`
    $('#tasks').prepend(html);

    const taskStatus = res.task_status;

    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}
