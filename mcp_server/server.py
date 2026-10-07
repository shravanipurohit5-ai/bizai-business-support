from mcp.server.fastmcp import FastMCP

from mcp_server.tools import (
    search_customer,
    search_product,
    get_order,
    check_stock,
    get_sales_report,
    cancel_order,
    create_return,
)

# Create MCP server
mcp = FastMCP("BizAI Business Server")


@mcp.tool()
def customer_search(name: str):
    """Search for a customer by name."""
    return search_customer(name)


@mcp.tool()
def product_search(name: str):
    """Search for a product by name."""
    return search_product(name)


@mcp.tool()
def order_details(order_id: int):
    """Get complete details of an order."""
    return get_order(order_id)


@mcp.tool()
def product_stock(product_name: str):
    """Check available stock for a product."""
    return check_stock(product_name)


@mcp.tool()
def sales_report():
    """Get overall business sales report."""
    return get_sales_report()


@mcp.tool()
def order_cancel(order_id: int):
    """Cancel an eligible order."""
    return cancel_order(order_id)


@mcp.tool()
def order_return(order_id: int):
    """Create a return request for a delivered order."""
    return create_return(order_id)


if __name__ == "__main__":
    print("🚀 BizAI MCP Server starting...")
    mcp.run()