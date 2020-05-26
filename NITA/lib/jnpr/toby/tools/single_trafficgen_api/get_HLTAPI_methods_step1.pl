#!/usr/bin/perl -w

# Creates comparison file between ixia and spirent overlapping HLTAPI functions/methods & parameters
# example: get_HLTAPI_methods_step1.pl > HLTAPI_method_comparison.tab

use strict;

my %ixia;
my %spirent;

my $FH;

open($FH, "<spirent.txt");
my %arglist = ();
my $state = 'unknown';
my %funclist = ();
my $next_line = 0;
my $function = '';
while (<$FH>) {
    my $line = $_;
    if ($line =~ /^Name:/) {
        $next_line = 1;
    } 
    if (($line =~ /^ sth::(\w+)/) && ($next_line == 1)) {
        $next_line = 0;
        my $prior_function = $function;
        $function = $1;
        if (defined $funclist{$function}) {
            next;
        }
        else {
            $funclist{$function} = 1;
        }
        if (scalar keys %arglist > 0) {
            foreach my $key (keys %arglist) {
                $spirent{$prior_function . "\t" . $key} = 1;
            }
            %arglist = ();
        }
        $state = 'definition';
    }
    elsif ($line =~ /^Synopsis:/) {
        $state = 'arg_synopsis';
    } 
    elsif (($line =~ /-([a-z]\w+)/) && ($state eq 'arg_synopsis')) {
        my $arg = $1;
        $arglist{$arg} = 1;
    }
    elsif ($line =~ /^Argument/) {
        $state = 'arg_details';
    }
}
if (scalar keys %arglist > 0) {
    foreach my $key (keys %arglist) {
        $spirent{$function . "\t" . $key} = 1;
    }
    %arglist = ();
}
close($FH);

### end SPIRENT and start IXIA ###

%arglist = ();
$state = 'unknown';
$function = '';

open($FH, "<ixia_robot.py");
while (<$FH>) {
    my $line = $_;
    if ($line =~ /^def (\w+)/) {
        my $prior_function = $function;
        $function = $1;
        if (scalar keys %arglist > 0) {
            foreach my $key (keys %arglist) {
                $ixia{$prior_function . "\t" . $key} = 1;
            }
            %arglist = ();
        }
        $state = 'definition';
    }
    elsif ($line =~ /^\s+Synopsis/) {
        $state = 'arg_synopsis';
    } 
    elsif (($line =~ /-([a-z]\w+)/) && ($state eq 'arg_synopsis')) {
        my $arg = $1;
        $arglist{$arg} = 1;
    }
    elsif ($line =~ /^\s+Argument/) {
        $state = 'arg_details';
    }
}
if (scalar keys %arglist > 0) {
    foreach my $key (keys %arglist) {
        $ixia{$function . "\t" . $key} = 1;
    }
    %arglist = ();
}
close($FH);

my %master_list;

foreach my $key (sort keys %spirent) {
    $master_list{$key} = 'spirent';
}
foreach my $key (sort keys %ixia) {
    if ($master_list{$key}) {
        $master_list{$key} = 'both';
    }
    else { 
        $master_list{$key} = 'ixia';
    }
}
foreach my $key (sort keys %master_list) {
    print $key . "\t" . $master_list{$key} . "\n";
}
