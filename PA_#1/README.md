Our goal in this assignment is to write regular expressions that extract
phone numbers and regular expressions that extract email addresses.
To start with a trivial example, given:
huangrh@cse.tamu.edu
we should return:
huangrh@cse.tamu.edu
But we also need to deal with more complex examples created by people trying to shield
their addresses, such as the following types of examples that we have all seen:
huangrh(at)cse.tamu.edu
huangrh at cse dot tamu dot edu
We should even handle examples that look like the following (as it appears on our screen;
we've used metachars on this page to make it display properly):
<script type="text/javascript">obfuscate('cse.tamu.edu','huangrh')</script>
Similarly, for phone numbers, we need to handle examples like the following:
Phone: (979) 862-2908
Tel (+1): 979-862-2908
<a href="contact.html">TEL</a> +1&thinsp;979&thinsp;862&thinsp;2908
all of which should return the following canonical form:
979-862-2908
