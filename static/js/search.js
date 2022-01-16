            function search() {
                let search = $('#searchValue').val()
                $.ajax({
                    type: "POST",
                    url: "/",
                    data: { searchWord_give: search },
                })
            }



