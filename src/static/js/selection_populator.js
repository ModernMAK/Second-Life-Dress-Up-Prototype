// mustache/handlebars are best served from node
//      But I hate setting it up, especially for prototypes

function update_preview_images()
{
    var bot = Cookies.get("data-bottom-id") ?? 0;
//    var bot = $("#preview-info").attr("data-bottom-id");
    var top = Cookies.get("data-top-id") ?? 0;
//    var top = $("#preview-info").attr("data-top-id");
    var src = "/preview?top=".concat(top).concat("&bot=").concat(bot);
    $("#preview-sidebar").attr("src",src);
    $("#preview-collapsable").attr("src",src);
}

function update_preview(attr_name, attr_val)
{
    const epoch_date = new Date(2147483647 * 1000);
    Cookies.set(attr_name, attr_val, {expires: epoch_date})
//    $("#preview-info").attr(attr_name,attr_val);
    update_preview_images();
}


function update_buttons(btn_class, attr_name, id_prefix)
{
    var selected = Cookies.get(attr_name) ?? "0";
    $(btn_class).children("img").removeClass("bg-primary");
    $(id_prefix.concat(selected)).children("img").addClass("bg-primary");
}

function setup_buttons(btn_class, attr_name, id_prefix)
{

    $(btn_class).click(
        function()
        {
            var id = $(this).attr(attr_name);
            update_preview(attr_name, id);
            update_buttons(btn_class,attr_name,id_prefix);
            return false;
        }
    );
    update_buttons(btn_class,attr_name,id_prefix);
}

function attach_populator(btn_id, endpoint, template_path, parser, btn_class, attr_name, id_prefix)
{
    $(btn_id).click(
        function(){
            $.ajax(endpoint).done(
                function(data)
                {
                    var parsed_data = parser(data);
                    $.get(template_path).done(
                        function(template){
                            var t = Handlebars.compile(template);
                            var html = t(parsed_data);
                            $("#selection-area").html(html);
                            setup_buttons(btn_class, attr_name, id_prefix)
                        }
                    );
                }
            );
            return false;
        }
    )
}



attach_populator("#tops-tab", "/tops","/js/templates/tops.handlebars",
    function(data)
    {
        var list = []
        for(var key in data)
        {
            var item = {
                'id': key,
                'img':data[key]
            }
            list.push(item)
        }
        return {"tops":list}
    },
    ".js-top-btn", "data-top-id", "#top-"
)

attach_populator("#bottoms-tab", "/bottoms","/js/templates/bottoms.handlebars",
    function(data)
    {
        var list = []
        for(var key in data)
        {
            var item = {
                'id': key,
                'img':data[key]
            }
            list.push(item)
        }
        return {"bottoms":list}
    },
    ".js-bottom-btn", "data-bottom-id", "#bottom-"
)

//setup_buttons(".js-top-btn")
update_preview_images()
$("#tops-tab").click()