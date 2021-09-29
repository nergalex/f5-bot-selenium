when CLIENTSSL_CLIENTHELLO priority 320 {
    if {[SSL::extensions exists -type 0]} {
        binary scan [SSL::extensions -type 0] @9A* sni_value
    } else {
        set sni_value {}
    }
    # log local0. "SNI: $sni_value"
}
when SERVERSSL_CLIENTHELLO_SEND priority 320 {

# SNI extension record as defined in RFC 3546/3.1
#
# - TLS Extension Type                =  int16( 0 = SNI )
# - TLS Extension Length              =  int16( $sni_length + 5 byte )
#    - SNI Record Length              =  int16( $sni_length + 3 byte)
#       - SNI Record Type             =   int8( 0 = HOST )
#          - SNI Record Value Length  =  int16( $sni_length )
#          - SNI Record Value         =    str( $sni_value )
#

# Calculate the length of the SNI value, Compute the SNI Record / TLS extension fields and add the result to the SERVERSSL_CLIENTHELLO

SSL::extensions insert [binary format SSScSa* 0 [expr { [set sni_length [string length $sni_value]] + 5 }] [expr { $sni_length + 3 }] 0 $sni_length $sni_value]

}
