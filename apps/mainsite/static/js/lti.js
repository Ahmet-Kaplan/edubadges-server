function Request() {

    this.poll = false;

    this.activatePoll = function () {
        this.poll = true;
        this.runPoll();
    };

    this.disablePoll = function () {
        this.poll = false;
    };

    this.runPoll = function () {
        var self = this;
        var poll = setTimeout(function () {
            $.ajax({
                url: '{{ check_login }}',
                success: function (response) {
                    console.log(response);
                    if(response['loggedin']){
                        window.location =$('#login-link').attr('next-url');
                    }
                },
                dataType: "json",
                complete: function () {
                    if (self.poll == false) {
                        clearTimeout(poll);
                    } else {
                        self.runPoll();
                    }
                }
            })
        }, 1000);
    };
}

$(document).ready(function () {
    $request = new Request();
    $request.activatePoll();
});