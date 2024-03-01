
var calendar; // 在全局作用域声明变量

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, { // 移除了var关键字
        initialView: 'dayGridMonth',
        events: '{% url "events" %}',
        eventContent: function(arg) {
            // 创建显示事件标题的元素
            var element = document.createElement('div');
            var title = document.createElement('div');
            title.innerText = arg.event.title;
            
            // 创建显示参与人的元素
            var participants = document.createElement('div');
            participants.innerText = "Participants: " + arg.event.extendedProps.participants.join(', ');
        
            element.appendChild(title);
            element.appendChild(participants);
        
            return { domNodes: [element] };
        },
    });
    calendar.render();
});

function deleteEvent(eventId) {
    $.ajax({
        type: "POST",
        url: "/delete_event/" + eventId + "/",
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function(response) {
            if(response.success) {
                alert("Event deleted successfully!");
                calendar.refetchEvents(); // 删除后重新获取事件
            }
        },
        error: function(xhr, errmsg, err) {
            alert("Error deleting event. Please try again.");
        },
    });
}

$(document).ready(function() {
    $('#eventForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "{% url 'add_event' %}",
            data: {
                title: $('#id_title').val(),
                start_time: $('#id_start_time').val(),
                end_time: $('#id_end_time').val(),
                description: $('#id_description').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response) {
                if(response.success) {
                    alert("Event added successfully!");
                    calendar.refetchEvents(); // 重新获取事件并刷新日历
                }
            },
            error: function(xhr, errmsg, err) {
                alert("Error adding event. Please try again.");
                console.log(xhr.responseText);  // 调试用
            },
        });
    });
});


$(document).ready(function() {
    $('#eventForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "{% url 'add_event' %}",
            data: {
                title: $('#id_title').val(),
                start_time: $('#id_start_time').val(),
                end_time: $('#id_end_time').val(),
                description: $('#id_description').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response) {
                if(response.success) {
                    alert("Event added successfully!");
                    calendar.refetchEvents(); // 重新获取事件并刷新日历
                }
            },
            error: function(xhr, errmsg, err) {
                alert("Error adding event. Please try again.");
                console.log(xhr.responseText);  // 调试用
            },
        });
    });
});

