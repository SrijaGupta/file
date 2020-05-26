#!/usr/bin/perl -w

use strict;

my $FH;

open($FH, "<ixia_robot.py");
my $state = 'unknown';
my $useless_arg_synopsis_data;

print "<h1>TOBY IXIA Keywords</h1>\n";
my @new_content;
my $api_supported = 1;
my %apis;
my $last_api;

while (<$FH>) {
    my $line = $_;
    $line =~ s/ n //g;
    $line =~ s/<\/?b>//g;
    $line =~ s/</&lt;/g;
    $line =~ s/>/&gt;/g;

    if ($line =~ /^\s+$/) {
        #do nothing
    }
#    elsif ($line =~ /NGPF API Support: No/) {
#        delete $apis{$last_api};
#        while($new_content[-1] !~ /font/) {
#            pop @new_content;
#        }
#        pop @new_content;
#        $api_supported = 0;
#    }
    elsif ($line =~ /^def (\w+)/) {
        $apis{$1} = 1;
        $last_api = $1;
        push @new_content, "<br><br>\n" .
                           '<font color="Green" size="6"><a name="' . $1 . '">' . $1 . "</a></font><br>\n" . 
                           'Execute Tester Command&nbsp;&nbsp;&nbsp;&nbsp;${rt_handle}&nbsp;&nbsp;&nbsp;&nbsp;command=' . $1 . "&nbsp;&nbsp;&nbsp;&nbsp;&lt;additional key=value arguments&gt;<br>\n";
        $state = 'declaration';
        $api_supported = 1;
    }
    elsif (!$api_supported) {
        #do nothing
    }
    elsif ($line =~ /^\s+Return Values/) {
        push @new_content, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Return Values</b>:<br>\n";
        $state = 'return_values';
    }
    elsif ($line =~ /^\s+Examples/) {
        $state = 'examples';
    }

    elsif ($state eq 'return_values') {
        $line =~ s/\s\s\s\s\s+value/, value/g;
        $line =~ s/\s\s/&nbsp;&nbsp;/g;
        push @new_content, '&nbsp;&nbsp;&nbsp;&nbsp;' . $line . '<br>';
    }
    elsif ($line =~ /""" (.*)\n/) {
        my $purpose = $1;
        $purpose =~ s/, starting and$//g;
        push @new_content, "&nbsp;&nbsp;&nbsp;&nbsp;<b>Purpose</b>:<br>\n";
        $purpose =~ s/\s\s\s\s+/<br>\n&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/g;
        $purpose =~ s/\n\s+?$//g;
        push @new_content, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' . $purpose . "<br>\n";
        $state = 'purpose';
    }
    elsif ($line =~ /^\s+Synopsis/) {
        push @new_content, "&nbsp;&nbsp;&nbsp;&nbsp;<b>Argument Summary</b>:";
        $useless_arg_synopsis_data = 1;
        $state = 'arg_synopsis';
    } 

    elsif ($line =~ /^\s+Argument/) {
        $state = 'arg_details';
        push @new_content, "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;<b>Argument Details</b>:<br>\n";
    }

    elsif (($line =~ /-([a-z]\w+)\s+(\w+)/) && ($state eq 'arg_synopsis')) {
        $useless_arg_synopsis_data = 0;
        push @new_content, "<br>\n";
        my $arg = '<font color=forestgreen><b>' . $1 . '</b></font>=' . $2;
        if ($arg =~ /CHOICES/) {
            $arg =~ s/CHOICES//g;
            my @line_segs = split('CHOICES',$line);
            my $choices = $line_segs[1];
            $choices =~ s/^\s+|\s+$//g;
            $choices =~ s/\s+/|/g; 
            $arg = $arg . $choices;
        }
        elsif ($arg =~ /REGEXP/) { 
            my @line_segs = split('REGEXP',$line);
            my $regexp = $line_segs[1];
            $regexp =~ s/^\s+|\s+$//g;
            $arg = $arg . ' ' .$regexp;
        }
        elsif ($arg =~ /RANGE/) { 
            my @line_segs = split('RANGE',$line);
            my $range = $line_segs[1];
            $range =~ s/^\s+|\s+$//g;
            $arg = $arg . ' ' . $range;
        } 

        $arg =~ s/\]$//g;
        push @new_content, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' . $arg;
    }
    elsif (($line =~ /^\s+CHOICES\s(\w+)/) && ($state eq 'arg_synopsis')) {
        push @new_content, "|$1";
    }
    elsif ($state eq 'arg_synopsis' && $useless_arg_synopsis_data == 0) {
        chomp $line;
        $line =~ s/^\s+//g;
        $line =~ s/\]+//g;
        push @new_content, ", $line";
    }
    elsif ($state eq 'arg_details') {
        $line =~ s/</&lt;/g;
        $line =~ s/>/&gt;/g;
        if ($line =~ /^\s+-[a-z]/) {
            $line =~ s/^\s+-/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color=forestgreen><b>/g;
            $line = $line . '</b></font>';
            if ($new_content[-1] !~ /<br>/) {
                $line = "<br>" . $line
            }
            push @new_content, $line . "<br>";
        }
        else {
            $line =~ s/^\s+//g;
            $line =~ s/\s+$//g;
            $line =~ s/\s+/ /g;
            if ($line =~ /^[a-z]/) {
                $new_content[-1] =~ s/<br>//g;
                $line = ' ' . $line . '<br>';
            }
            else {
                $line = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' . $line . "<br>";
            }
            push @new_content, $line;
        }
    }
}
push @new_content, "<br><br>\n\n";


foreach my $api_name (sort keys %apis) {
    print('<li>Execute Tester Command&nbsp;&nbsp;&nbsp;&nbsp;${rt_handle}&nbsp;&nbsp;&nbsp;&nbsp;command=<a href="#' . $api_name . '">' . $api_name . "</a></li>");
}

#print join('', @new_content);
#exit;

my $page = join('', @new_content);
$page =~ s/\n//g;
my @lines = split('<br>', $page);

for (my $i = 0; $i < scalar @lines; ++$i) {
    $lines[$i] = $lines[$i] . '<br>';

    my @line_segs = split(/\s+/,$lines[$i]);
    my $shortened_line = '';

    foreach my $word (@line_segs) {
        if (length($shortened_line) >= 250) {
            my $indent = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
            $shortened_line = $shortened_line . "<br>$indent";
            print $shortened_line;
            $shortened_line = '';
        } 
        else {
            $shortened_line = $shortened_line . " " . $word;
            if ($shortened_line =~ /<br>/) {
                print $shortened_line;
                $shortened_line = '';
            }
        } 
    }
}    
#print join('', @new_content);


