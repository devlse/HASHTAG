console.log("fefef")
            function makeSearch() {
                let search = $('#searchValue').val()
                $.ajax({
                    type: "POST",
                    url: "/",
                    data: { searchWord_give: search},
                    success: function (response) {
                        alert(response["msg"]);
                        window.location.reload();
                    }
                })
            }

