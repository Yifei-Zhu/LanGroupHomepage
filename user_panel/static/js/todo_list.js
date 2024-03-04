document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('new-todo-form');
    const titleInput = document.getElementById('new-todo-title');
    const descriptionInput = document.getElementById('new-todo-description');
    const todoList = document.getElementById('todo-list');

    // 从服务器加载ToDo项
    function loadTodos() {
        fetch('/todos/')
        .then(response => response.json())
        .then(data => {
            data.forEach(todo => addTodoToDOM(todo));
            makeItemsDraggable(); // 调用此函数以使加载的待办事项可拖拽
        });
    }

    // 添加新ToDo项到DOM
    function addTodoToDOM(todo) {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="todo-item">
                <span class="${todo.completed ? 'completed' : ''}">${todo.title}: ${todo.description}</span>
                <button class="delete-todo" data-id="${todo.id}">Delete</button>
            </div>
        `;
        todoList.appendChild(li);
        li.querySelector('.delete-todo').addEventListener('click', function() {
            deleteTodo(todo.id);
        });
        makeItemsDraggable();
    }

    // 创建新的ToDo项
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const title = titleInput.value.trim();
        const description = descriptionInput.value.trim();

        if (title && description) {
            fetch('/todo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // 获取CSRF令牌
                },
                body: JSON.stringify({title: title, description: description})
            })
            .then(response => response.json())
            .then(todo => {
                addTodoToDOM(todo); // 将新ToDo项添加到DOM
                titleInput.value = '';
                descriptionInput.value = '';
            });
        }
    });

    // 删除ToDo项
    function deleteTodo(todoId) {
        fetch(`/todo/${todoId}/`, {
            method: 'DELETE',
    
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // 获取CSRF令牌
            }
        })
        .then(() => {
            document.querySelector(`button[data-id="${todoId}"]`).parentElement.parentElement.remove();
        });
    }

    // 辅助函数：获取Cookie值
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function makeItemsDraggable() {
        const items = document.querySelectorAll('li'); // 获取所有待办事项
        items.forEach(item => {
            item.setAttribute('draggable', true); // 设置为可拖动
    
            item.addEventListener('dragstart', function(e) {
                draggedItem = this; // 记录当前被拖动的项
                setTimeout(() => (this.style.opacity = "0.5"), 0); // 拖动时透明度变化，提升用户体验
            });
    
            item.addEventListener('dragend', function(e) {
                setTimeout(() => (this.style.opacity = "1"), 0); // 恢复透明度
                draggedItem = null; // 清除记录
                items.forEach(item => item.classList.remove('drag-over')); // 清除所有目标高亮样式
                saveTodos(); // 拖拽结束后保存新的顺序
            });
    
            item.addEventListener('dragover', function(e) {
                e.preventDefault(); // 必须阻止默认行为来允许放置
            });
    
            item.addEventListener('dragenter', function(e) {
                e.preventDefault();
                this.classList.add('drag-over'); // 应用目标高亮样式
            });
    
            item.addEventListener('dragleave', function(e) {
                this.classList.remove('drag-over'); // 移除目标高亮样式
            });
    
            item.addEventListener('drop', function(e) {
                this.classList.remove('drag-over'); // 移除目标高亮样式
                if (this !== draggedItem) {
                    let allItems = Array.from(document.querySelectorAll('li'));
                    let draggedIndex = allItems.indexOf(draggedItem);
                    let targetIndex = allItems.indexOf(this);
    
                    if (draggedIndex < targetIndex) {
                        this.parentNode.insertBefore(draggedItem, this.nextSibling); // 放置在目标项之后
                    } else {
                        this.parentNode.insertBefore(draggedItem, this); // 放置在目标项之前
                    }
    
                    // 由于元素位置发生变化，需要重新调用 makeItemsDraggable 来更新事件监听
                    makeItemsDraggable();
                }
            });
        });
    }
    
    
    loadTodos(); // 页面加载时从服务器加载ToDo项
});


