<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
   <xsl:output method="text" />
   <xsl:variable name="xslversion" select="'2009-07-15-1119716'"/>

   <xsl:template match="/">
      <xsl:text># Amazon Web Services
# Virtual Private Cloud
#
# AWS utilizes unique identifiers to manipulate the configuration of 
# a VPN Connection. Each VPN Connection is assigned a VPN Connection Identifier
# and is associated with two other identifiers, namely the 
# Customer Gateway Identifier and the Virtual Private Gateway Identifier.
#
# Your VPN Connection ID  		    : </xsl:text>
        <xsl:value-of select="vpn_connection/@id"/><xsl:text>
# Your Virtual Private Gateway ID           : </xsl:text>
        <xsl:value-of select="vpn_connection/vpn_gateway_id"/><xsl:text>
# Your Customer Gateway ID 		    : </xsl:text>
        <xsl:value-of select="vpn_connection/customer_gateway_id"/><xsl:text>
#
# This configuration consists of two tunnels. Both tunnels must be 
# configured on your Customer Gateway.
#
#
</xsl:text>
      <xsl:apply-templates select="vpn_connection" />
      <xsl:text>
# Additional Notes and Questions</xsl:text>
      <xsl:text>
#  - Amazon Virtual Private Cloud Getting Started Guide: 
#       http://docs.amazonwebservices.com/AmazonVPC/latest/GettingStartedGuide
#  - Amazon Virtual Private Cloud Network Administrator Guide: 
#       http://docs.amazonwebservices.com/AmazonVPC/latest/NetworkAdminGuide
#  - XSL Version: </xsl:text><xsl:value-of select="$xslversion"/><xsl:text>
      </xsl:text>
   </xsl:template>

   <!-- VPN Connection -->
   <xsl:template match="vpn_connection">
      <xsl:apply-templates select="ipsec_tunnel">
         <xsl:with-param name="cgwid" select="./customer_gateway_id" />
         <xsl:with-param name="vgwid" select="./vpn_gateway_id" />
      </xsl:apply-templates>
   </xsl:template> <!-- VPN Connection -->

   <!-- IPSec Tunnel -->
   <xsl:template match="vpn_connection/ipsec_tunnel">
      <xsl:param name="cgwid"/>
      <xsl:param name="vgwid"/>
      <xsl:variable name="id" select="concat(./../@id, '-', string(position()))"/>
      <xsl:variable name="peer" select="./vpn_gateway/tunnel_inside_address/ip_address" />
      <xsl:variable name="gateway" select="./vpn_gateway/tunnel_outside_address/ip_address" />
      <xsl:variable name="cgwip" select="./customer_gateway/tunnel_outside_address/ip_address" />

      <xsl:variable name="pgwcidr"
         select="concat('/',./vpn_gateway/tunnel_inside_address/network_cidr)" />
      <xsl:variable name="pgwaddr" select="concat($peer,$pgwcidr)" />
      <xsl:variable name="cgwcidr"
         select="concat('/', ./customer_gateway/tunnel_inside_address/network_cidr)" />
      <xsl:variable name="cgwaddr" 
         select="concat(./customer_gateway/tunnel_inside_address/ip_address, $cgwcidr)" />
      <xsl:variable name="tunintf" select="concat('st0.',string(position()))" />

<xsl:text># --------------------------------------------------------------------------------
# IPSec Tunnel #</xsl:text><xsl:value-of select="position()"/><xsl:text>
# --------------------------------------------------------------------------------
</xsl:text>

      <xsl:apply-templates select="./ike">
         <xsl:with-param name="id" select="$id" />
         <xsl:with-param name="gateway" select="$gateway" />
         <xsl:with-param name="cgwip" select="$cgwip" />
         <xsl:with-param name="cgwid" select="$cgwid" />
      </xsl:apply-templates>

      <xsl:apply-templates select="./ipsec">
         <xsl:with-param name="id" select="$id" />
         <xsl:with-param name="tunintf" select="$tunintf" />
      </xsl:apply-templates>
      <xsl:text>
# #3: Tunnel Interface Configuration
#
</xsl:text>

      <xsl:text>
# The tunnel interface is configured with the internal IP address.
#
set interfaces </xsl:text><xsl:value-of select="$tunintf"/>
      <xsl:text> family inet address </xsl:text><xsl:value-of select="$cgwaddr"/>
      <xsl:text>
set interfaces </xsl:text><xsl:value-of select="$tunintf"/>
      <xsl:text> family inet mtu 1436
set security zones security-zone trust interfaces </xsl:text><xsl:value-of select="$tunintf"/>
      <xsl:text>

# The security zone protecting external interfaces of the router must be 
# configured to allow IKE traffic inbound.
#
set security zones security-zone untrust host-inbound-traffic system-services ike

# The security zone protecting internal interfaces (including the logical 
# tunnel interfaces) must be configured to allow BGP traffic inbound.
#
set security zones security-zone trust host-inbound-traffic protocols bgp
</xsl:text>
      <xsl:apply-templates select="./ipsec/tcp_mss_adjustment"/>
<xsl:choose>
   <xsl:when test="(./../vpn_connection_attributes) = 'NoBGPVPNConnection'">
   <xsl:text>
# --------------------------------------------------------------------------------
# #4: Static Route Configuration
#
# VPN monitoring is used in order to provide failover with multiple tunnels. If the primary tunnel fails, the redundant tunnel will automatically be used.
#
</xsl:text>
      <xsl:text>set security ipsec vpn </xsl:text><xsl:value-of select="$id"/><xsl:text> vpn-monitor source-interface </xsl:text>
      <xsl:value-of select="$tunintf"/>
      <xsl:text> 
set security ipsec vpn </xsl:text><xsl:value-of select="$id"/><xsl:text> vpn-monitor destination-ip </xsl:text><xsl:value-of select="$peer"/><xsl:text>

# Your Customer Gateway needs to set a static route for the prefix corresponding to your VPC on the tunnel.
# An example for a VPC with the prefix 10.0.0.0/16 is provided below
# set routing-options static route 10.0.0.0/16 next-hop </xsl:text><xsl:value-of select="$tunintf"/>
   </xsl:when>
<xsl:otherwise>
<xsl:text>
# --------------------------------------------------------------------------------
# #4: Border Gateway Protocol (BGP) Configuration
#                                                                                     
# BGP is used within the tunnel to exchange prefixes between the
# Virtual Private Gateway and your Customer Gateway. The Virtual Private Gateway    
# will announce the prefix corresponding to your VPC.
#            
# Your Customer Gateway may announce a default route (0.0.0.0/0), 
# which can be done with the EXPORT-DEFAULT policy. 
#
# To advertise additional prefixes to Amazon VPC, add additional prefixes to the "default" term
# EXPORT-DEFAULT policy. Make sure the prefix is present in the routing table of the device with 
# a valid next-hop.
#                                                                               
# The BGP timers are adjusted to provide more rapid detection of outages.       
# 
# The local BGP Autonomous System Number (ASN) (</xsl:text><xsl:value-of select="./customer_gateway/bgp/asn"/>
      <xsl:text>) is configured
# as part of your Customer Gateway. If the ASN must be changed, the 
# Customer Gateway and VPN Connection will need to be recreated with AWS.
#
# We establish a basic route policy to export a default route to the
# Virtual Private Gateway.       
#
set policy-options policy-statement EXPORT-DEFAULT term default from route-filter 0.0.0.0/0 exact                                                               
set policy-options policy-statement EXPORT-DEFAULT term default then accept     
set policy-options policy-statement EXPORT-DEFAULT term reject then reject

set protocols bgp group ebgp type external

</xsl:text>

      <xsl:variable name="base" select="concat('set protocols bgp group ebgp neighbor ', $peer)"/>
      <xsl:value-of select="$base"/><xsl:text> export EXPORT-DEFAULT 
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> peer-as </xsl:text>
      <xsl:value-of select="./vpn_gateway/bgp/asn" /><xsl:text>
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> hold-time </xsl:text>
      <xsl:value-of select="./vpn_gateway/bgp/hold_time" /><xsl:text>
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> local-as </xsl:text>
      <xsl:value-of select="./customer_gateway/bgp/asn" />
</xsl:otherwise>
</xsl:choose><xsl:text>
#
</xsl:text>
   </xsl:template> <!-- IPSec Tunnel -->

   <!-- IKE Settings -->
   <xsl:template match="ipsec_tunnel/ike">
      <xsl:param name="id" />
      <xsl:param name="gateway" />
      <xsl:param name="cgwip" />
      <xsl:param name="cgwid" />

      <xsl:variable name="ikepol" select="concat('ike-pol-', $id)" />
      <xsl:variable name="ikeprop" select="concat('ike-prop-', $id)" />

      <xsl:text># #1: Internet Key Exchange (IKE) Configuration
#
# A proposal is established for the supported IKE encryption, 
# authentication, Diffie-Hellman, and lifetime parameters.
#
</xsl:text>
      <xsl:variable name="base"
         select="concat('set security ike proposal ',$ikeprop)" />
      <xsl:value-of select="$base" /><xsl:text> authentication-method pre-shared-keys 
</xsl:text>
      <xsl:call-template name='common-ike-ipsec'>
         <xsl:with-param name="base" select="$base" />
      </xsl:call-template>
      <xsl:value-of select="$base" /><xsl:text> dh-group </xsl:text>
      <xsl:value-of select="./perfect_forward_secrecy" />
      <xsl:text>

# An IKE policy is established to associate a Pre Shared Key with the  
# defined proposal.
#
set security ike policy </xsl:text>
      <xsl:value-of select="$ikepol" /><xsl:text> mode </xsl:text>
      <xsl:value-of select="./mode" />
      <xsl:text> 
set security ike policy </xsl:text>
      <xsl:value-of select="$ikepol" /><xsl:text> proposals </xsl:text>
      <xsl:value-of select="$ikeprop" />
      <xsl:text>
set security ike policy </xsl:text>
      <xsl:value-of select="$ikepol" /><xsl:text> pre-shared-key ascii-text </xsl:text>
      <xsl:value-of select="./pre_shared_key" />

      <xsl:text>

# The IKE gateway is defined to be the Virtual Private Gateway. The gateway 
# configuration associates a local interface, remote IP address, and
# IKE policy.
#
# This example shows the outside of the tunnel as interface ge-0/0/0.0.
# This should be set to the interface that IP address </xsl:text>
      <xsl:value-of select="$cgwip" /><xsl:text> is
# associated with.
# This address is configured with the setup for your Customer Gateway.
#
# If the address changes, the Customer Gateway and VPN Connection must be recreated.
#
set security ike gateway gw-</xsl:text>
      <xsl:value-of select="$id" /><xsl:text> ike-policy </xsl:text>
      <xsl:value-of select="$ikepol" />
      <xsl:text>
set security ike gateway gw-</xsl:text>
      <xsl:value-of select="$id" /><xsl:text> external-interface ge-0/0/1.0
set security ike gateway gw-</xsl:text>
      <xsl:value-of select="$id" /><xsl:text> address </xsl:text>
      <xsl:value-of select="$gateway" />

#set static routing options through gateway 10.0.2.1 for both the tunnel addresses

<xsl:text>
set routing-options static route </xsl:text>
      <xsl:value-of select="$gateway" /><xsl:text> next-hop 10.0.2.1 </xsl:text>

      <xsl:text>

# Troubleshooting IKE connectivity can be aided by enabling IKE tracing.
# The configuration below will cause the router to log IKE messages to
# the 'kmd' log. Run 'show messages kmd' to retrieve these logs.
# set security ike traceoptions file kmd
# set security ike traceoptions file size 1024768
# set security ike traceoptions file files 10
# set security ike traceoptions flag all

</xsl:text>
   </xsl:template> <!-- IKE Settings -->

   <!-- IPSEC Settings -->
   <xsl:template match="ipsec_tunnel/ipsec">
      <xsl:param name="id" />
      <xsl:param name="tunintf" />

      <xsl:variable name="ipsecpol" select="concat('ipsec-po-',$id)" />
      <xsl:variable name="ipsecprop" select="concat('ipsec-pr-',$id)" />

      <xsl:variable name="base"
         select="concat('set security ipsec proposal ', $ipsecprop)" />

      <xsl:text># #2: IPSec Configuration
#
# The IPSec proposal defines the protocol, authentication, encryption, and
# lifetime parameters for our IPSec security association.
#
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> protocol </xsl:text>
      <xsl:value-of select="./protocol" /><xsl:text>
</xsl:text>

      <xsl:call-template name='common-ike-ipsec'>
         <xsl:with-param name="base" select="$base" />
      </xsl:call-template>

      <xsl:text>
# The IPSec policy incorporates the Diffie-Hellman group and the IPSec
# proposal.
#
set security ipsec policy </xsl:text><xsl:value-of select="$ipsecpol" />
      <xsl:text> perfect-forward-secrecy keys </xsl:text>
      <xsl:value-of select="./perfect_forward_secrecy" />

      <xsl:text>
set security ipsec policy </xsl:text><xsl:value-of select="$ipsecpol" />
      <xsl:text> proposals ipsec-pr-</xsl:text>
      <xsl:value-of select="$id" /><xsl:text>
</xsl:text>

      <xsl:text>
# A security association is defined here. The IPSec Policy and IKE gateways
# are associated with a tunnel interface (</xsl:text><xsl:value-of select="$tunintf" /><xsl:text>).
# The tunnel interface ID is assumed; if other tunnels are defined on
# your router, you will need to specify a unique interface name 
# (for example, st0.10).
#
set security ipsec vpn </xsl:text>
      <xsl:value-of select="$id" />
      <xsl:text> bind-interface </xsl:text><xsl:value-of select="$tunintf" />
      <xsl:text>
set security ipsec vpn </xsl:text>
      <xsl:value-of select="$id" />
      <xsl:text> ike gateway gw-</xsl:text><xsl:value-of select="$id" />
      <xsl:text>
set security ipsec vpn </xsl:text>
      <xsl:value-of select="$id" />
      <xsl:text> ike ipsec-policy </xsl:text><xsl:value-of select="$ipsecpol" />
      <xsl:apply-templates select="clear_df_bit">
         <xsl:with-param name="id" select="$id" />
      </xsl:apply-templates>
      <xsl:apply-templates select="dead_peer_detection">
         <xsl:with-param name="id" select="$id" />
      </xsl:apply-templates><xsl:text>
</xsl:text>
   </xsl:template> <!-- IPSec -->

   <xsl:template match="ipsec/tcp_mss_adjustment">
      <xsl:text>
# This option causes the router to reduce the Maximum Segment Size of
# TCP packets to prevent packet fragmentation.
#
set security flow tcp-mss ipsec-vpn mss </xsl:text><xsl:value-of select="."/><xsl:text>
</xsl:text>
   </xsl:template>

   <xsl:template match="ipsec/clear_df_bit">
      <xsl:param name="id" />
      <xsl:text>
set security ipsec vpn </xsl:text>
      <xsl:value-of select="$id" />
      <xsl:text> df-bit clear 
</xsl:text>
   </xsl:template>

   <xsl:template match="ipsec/dead_peer_detection">
      <xsl:param name="id" />
      <xsl:text>
# This option enables IPSec Dead Peer Detection, which causes periodic
# messages to be sent to ensure a Security Association remains operational.
#
set security ike gateway gw-</xsl:text>
      <xsl:value-of select="$id" /><xsl:text> dead-peer-detection interval 10 threshold 3
</xsl:text>
   </xsl:template>

   <!-- IKE/IPSec common parameters -->
   <xsl:template name="common-ike-ipsec">
      <xsl:param name="base" />
      <xsl:value-of select="$base" /><xsl:text> authentication-algorithm </xsl:text>
      <xsl:value-of select="./authentication_protocol" />
      <xsl:text>
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> encryption-algorithm </xsl:text>
      <xsl:value-of select="./encryption_protocol" />
      <xsl:text>
</xsl:text>
      <xsl:value-of select="$base" /><xsl:text> lifetime-seconds </xsl:text>
      <xsl:value-of select="./lifetime" />
      <xsl:text>
</xsl:text>
   </xsl:template> <!-- Common IKE/IPSec -->

</xsl:stylesheet>
