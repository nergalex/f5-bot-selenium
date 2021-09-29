when RULE_INIT {
  set static::shape_headers "Xa4vrhYP3Q-a,Xa4vrhYP3Q-b,Xa4vrhYP3Q-c,Xa4vrhYP3Q-d,Xa4vrhYP3Q-f,Xa4vrhYP3Q-z"
  set static::iapp_name "XXXXX"
  set static::cors_debug 0
}

when HTTP_REQUEST priority 100 {

  # OPTION
  if { [HTTP::method] equals "OPTIONS" } {
    set http_host [HTTP::host]
    set normalized_path [HTTP::path -normalized]
    set source_uri "[string tolower $http_host]$normalized_path"
    if { $static::cors_debug } {
        log local0. "Source URI: ${source_uri}"
    }
    set ibd_classes [list "/Common/${static::iapp_name}_ShapeGETEndpoints" "/Common/${static::iapp_name}_ShapePOSTEndpoints" "/Common/${static::iapp_name}_ShapePUTEndpoints" "/Common/${static::iapp_name}_ShapeANYEndpoints" "/Common/${static::iapp_name}_ShapeANYEndpoints"]

    # lookup for a matched endpoint
    foreach {ibd_class} ${ibd_classes}  {
      if {[class exists ${ibd_class}]} {
        foreach {endpoint} [class names ${ibd_class}]  {
          if { (${source_uri} matches_glob ${endpoint}) } {
              set cors_fix 1
              if { $static::cors_debug } {
                  log local0. "matched_URI=${endpoint}"
                  log local0. "matched_class=${ibd_class}"
              }
          }
        }
      }
    }
  }
}

when HTTP_RESPONSE priority 100 {
  if { [info exists cors_fix] } {
    set header_val [HTTP::header "Access-Control-Allow-Headers"]
    append header_val "," ${static::shape_headers}
    HTTP::header replace "Access-Control-Allow-Headers" ${header_val}
  }
}