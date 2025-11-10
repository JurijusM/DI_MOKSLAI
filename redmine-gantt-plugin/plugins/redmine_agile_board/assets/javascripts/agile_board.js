document.addEventListener('DOMContentLoaded', () => {
  const board = document.querySelector('.agile-board');
  if (!board) { return; }

  board.querySelectorAll('.agile-board__card').forEach(draggable => {
    draggable.addEventListener('dragstart', handleDragStart);
  });

  board.querySelectorAll('.agile-board__cards').forEach(list => {
    list.addEventListener('dragover', handleDragOver);
    list.addEventListener('drop', handleDrop);
  });
});

function handleDragStart(event) {
  event.dataTransfer.setData('text/plain', event.currentTarget.dataset.issueId);
  event.dataTransfer.effectAllowed = 'move';
}

function handleDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = 'move';
}

function handleDrop(event) {
  event.preventDefault();

  const list = event.currentTarget;
  const issueId = event.dataTransfer.getData('text/plain');
  const card = document.querySelector(.agile-board__card[data-issue-id=""]);
  if (!card) { return; }

  list.appendChild(card);
  const columnId = list.closest('.agile-board__column').dataset.columnId;
  const projectId = list.closest('.agile-board').dataset.projectId;

  fetch(/projects//agile_board/update_status, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': getMetaValue('csrf-token')
    },
    body: JSON.stringify({ issue_id: issueId, column_id: columnId })
  }).then(response => {
    if (!response.ok) {
      response.json().then(json => alert(json.errors.join('\n')));
    }
  }).catch(error => console.error(error));
}

function getMetaValue(name) {
  const element = document.querySelector(meta[name=""]);
  return element ? element.getAttribute('content') : '';
}
