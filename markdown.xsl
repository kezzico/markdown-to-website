<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="document">
<HTML>
<HEAD>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta property="og:type" content="website" />

	<!-- title from markdown meta -->
	<title>
		<xsl:value-of select="@title" />
	</title>
	
	<!-- title from markdown meta -->
	<meta property="og:title">
		<xsl:attribute name="content"> <xsl:value-of select="@title"/> </xsl:attribute>
	</meta>

	<!-- description from markdown meta -->
	<meta property="og:description">
		<xsl:attribute name="content"> <xsl:value-of select="@description"/> </xsl:attribute>
	</meta>

	<!-- keywords from markdown meta -->
	<meta name="keywords">
		<xsl:attribute name="content"> <xsl:value-of select="@keywords"/> </xsl:attribute>
	</meta>
</HEAD>
<BODY>
	<header>
	</header>

	<main>
		<xsl:apply-templates select="content"/>
	</main>

	<footer>
	</footer>
</BODY>
</HTML>
</xsl:template>

<xsl:template match="strong">
	<strong> <xsl:apply-templates match="*" /> </strong>
</xsl:template>

<xsl:template match="em">
	<em> <xsl:value-of select="." /> </em>
</xsl:template>


<xsl:template match="p">
	<p> <xsl:apply-templates match="*" /> </p>
</xsl:template>

<xsl:template match="br">
	<br />
</xsl:template>

<xsl:template match="blockquote">
	<blockquote>
		<xsl:apply-templates match="*" />
	</blockquote>
</xsl:template>

<xsl:template match="img">
	<div class="image-wrapper">
		<img src="{@src}" alt="{@alt}" />
	</div>
</xsl:template>

<xsl:template match="h1">
	<h1> <xsl:value-of select="." /> </h1 >
</xsl:template>

<xsl:template match="h2">
	<h2> <xsl:value-of select="." /> </h2>
</xsl:template>

<xsl:template match="h3">
	<h3> <xsl:value-of select="." /> </h3>
</xsl:template>

<xsl:template match="h4">
	<h4> <xsl:value-of select="." /> </h4>
</xsl:template>

<xsl:template match="hr">
	<hr />
</xsl:template>

<xsl:template match="a">
	<xsl:choose>
    <xsl:when test="starts-with(@href, 'http') or starts-with(@href, 'https')">
		<a href="{@href}" target="_blank">
			<xsl:value-of select="." />
      </a>
    </xsl:when>
    <!-- For internal links or other links -->
    <xsl:otherwise>
      <a href="{@href}">
		<xsl:value-of select="." />
      </a>
    </xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="ul">
	<ul class="list">
		<xsl:apply-templates match="ul/*" />
	</ul>
</xsl:template>

<xsl:template match="ul/li">
  <li>
	<xsl:apply-templates match="*" />
  </li>
</xsl:template>

<xsl:template match="ol">
	<ol class="list">
		<xsl:apply-templates match="ol/*" />
	</ol>
</xsl:template>

<xsl:template match="ol/li">
  <li>
	<xsl:apply-templates match="*" />
  </li>
</xsl:template>

<xsl:template match="pre/code">
<div class="code">
	<pre>
		<xsl:apply-templates match="*" />
	</pre>
</div>
</xsl:template>

<xsl:template match="code">
<span class="code">
	<xsl:apply-templates match="*" />
</span>
</xsl:template>

<xsl:template match="table">
	<table>
		<xsl:copy-of select="node()" />
	</table>
</xsl:template>

<xsl:template match="figcaption">
</xsl:template>

</xsl:stylesheet>

