// Function to update event table based on filters
function updateEventTable() {
    var formData = $('#eventFilterForm').serialize();
    $.get('/filter_events', formData, function (data) {
        // Update the event table content
        $('#eventTable tbody').html(data);
    });
}

// Function to update fighter table based on filters
function updateFighterTable() {
    var formData = $('#fighterRankingsForm').serialize();
    $.get('/filter_fighters', formData, function (data) {
        // Update the fighter table content
        $('#fighterTable tbody').html(data);
    });
}

// Event filter form submission
$('#submit_event_filter').click(function (e) {
    e.preventDefault(); // Prevent default form submission
    updateEventTable();
});

// Fighter rankings form submission
$('#submit_fighter_filter').click(function (e) {
    e.preventDefault(); // Prevent default form submission
    updateFighterTable();
});
