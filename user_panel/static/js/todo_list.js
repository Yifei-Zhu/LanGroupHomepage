document.addEventListener('DOMContentLoaded', function () {
    console.log('Loading todos...')
    const form = document.getElementById('new-todo-form');
    const titleInput = document.getElementById('new-todo-title');
    const descriptionInput = document.getElementById('new-todo-description');
    const todoList = document.getElementById('todo-list');

    // 加载待办事项时调用 makeItemsDraggable 和 updateTodoOrder
    function loadTodos() {
        console.log('Loading todos...');
        fetch('/todos/')
            .then(response => response.json())
            .then(data => {
                data.forEach(todo => addTodoToDOM(todo)); // 确保 todo 参数包含正确的 completed 状态
                makeItemsDraggable();
            });
    }

    // 添加新ToDo项到DOM
    function addTodoToDOM(todo) {
        console.log("Todo completed status:", todo.completed); // 打印待办事项的完成状态
    
        const li = document.createElement('li');
        li.dataset.id = todo.id;
        const isChecked = todo.completed ? 'checked' : '';
        const isCompletedClass = todo.completed ? 'completed' : '';
        li.innerHTML = `
            <div class="todo-item">
                <input type="checkbox" class="toggle-completed" ${isChecked}>
                <span class="${isCompletedClass}">${todo.title}: ${todo.description}</span>
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
    
        // 检查title或description是否为空
        if (!title || !description) {
            // 如果任何一个为空，则弹出提醒
            alert('Title and description cannot be empty!');
            return; // 阻止进一步执行
        }
    
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
            updateTodoOrder(); // 删除待办事项后更新顺序
        });
    }

    // 事件委托来监听复选框的变化
    document.getElementById('todo-list').addEventListener('change', function(e) {
        if (e.target.classList.contains('toggle-completed')) {
            const todoId = e.target.closest('li').getAttribute('data-id'); // 从 data-id 属性获取 ID
            const completed = e.target.checked;
            fetch(`/toggle-todo-completed/${todoId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ completed: completed }),
            })
            .then(response => {
                if (response.ok) {
                    console.log('Todo completion status updated');
                } else {
                    console.error('Error updating todo completion status');
                }
            });
        }
    });


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
    
    function updateTodoOrder() {
        const todos = Array.from(document.querySelectorAll('#todo-list li')).map((item, index) => {
            return {
                id: item.dataset.id, // 从data-id属性中获取待办事项的ID
                order: index
            };
        });
    
        fetch('/update_todo_order/', { // 确保这个URL是正确的
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // 确保这个函数能正确获取CSRF令牌
            },
            body: JSON.stringify({todos: todos})
        })
        .then(response => {
            if (response.ok) {
                console.log('Order updated successfully');
            } else {
                console.error('Failed to update order');
            }
        });
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
                // 调用 updateTodoOrder 来更新数据库中的顺序
                updateTodoOrder();
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



