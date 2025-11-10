import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Hybrid Cloud Architecture')
# FIX 1: Move the graph label (title) to the top ('t')
dot.attr(rankdir='TB', newrank='true', label='Home Hybrid Cloud Architecture', fontsize='24', fontname='Helvetica', labelloc='t') 

# --- Node Styles (Professional/Muted) ---
server_style = {'shape': 'box3d', 'style': 'filled', 'fillcolor': '#EEEEEE', 'fontname': 'Helvetica'}
storage_node_style = {'shape': 'cylinder', 'style': 'filled', 'fillcolor': '#D9EDF7', 'fontname': 'Helvetica'} 
service_style = {'shape': 'ellipse', 'style': 'filled', 'fillcolor': '#D4EDDA', 'fontname': 'Helvetica'}
container_style = {'shape': 'box', 'style': 'filled', 'fillcolor': '#FFF3CD', 'fontname': 'Helvetica'}
device_style = {'shape': 'octagon', 'style': 'filled', 'fillcolor': '#F0E68C', 'fontname': 'Helvetica'}
pc_style = {'shape': 'box', 'style': 'filled', 'fillcolor': '#E0E0E0', 'fontname': 'Helvetica'}

# --- Cluster Colors (Hierarchical) ---
cloud_cluster_color = '#CCE5FF' 
tailscale_cluster_fill = '#E7DBF9' 
tailscale_cluster_border = '#B8A6D9' 
home_network_cluster_color = '#E6E6E6' 

# --- Cloud Cluster (External Compute) ---
with dot.subgraph(name='cluster_cloud') as c:
    c.attr(label='Cloud (Off-Site)', style='filled', color='#5E5E5E', fillcolor=cloud_cluster_color, fontsize='18', fontname='Helvetica', peripheries='1')
    
    with c.subgraph(name='cluster_seedbox') as sb:
        sb.attr(label='Cloud VM (Seedbox)', **server_style)
        sb.node('seedbox_qbit', 'qBittorrent', **service_style)
        sb.node('seedbox_ftp', 'FTP Server', **service_style)

# --- Tailscale Mesh Cluster (The Security/Access Plane) ---
with dot.subgraph(name='cluster_tailscale') as t:
    t.attr(label='Tailscale Mesh Network (Overlay)', style='filled', color=tailscale_cluster_border, fillcolor=f'{tailscale_cluster_fill}:white', gradientangle='90', fontsize='20', fontname='Helvetica')
    
    # --- Home Network Cluster (The Core Infrastructure) ---
    with t.subgraph(name='cluster_home') as h:
        h.attr(label='Home Network (LAN)', style='filled', color='#5E5E5E', fillcolor=home_network_cluster_color, fontsize='16', fontname='Helvetica')
        
        # --- Server: Pluto ---
        with h.subgraph(name='cluster_pluto') as p:
            p.attr(label='Pluto (Fedora NAS)', **server_style)
            p.node('pluto_cockpit', 'Cockpit Mgmt', **service_style)

            # LVM Storage Subgraph (NFS Server inside cylinder)
            with p.subgraph(name='cluster_pluto_storage') as ps_sub:
                ps_sub.attr(label='12TB LVM Storage (/mnt/media)', **storage_node_style)
                ps_sub.node('pluto_nfs', 'NFS Server', **service_style)

        # --- Server: Mars ---
        with h.subgraph(name='cluster_mars') as m:
            m.attr(label='Mars (Arch Linux, Docker Host)', **server_style)
            m.node('mars_mount', 'NFS Client Mount Point', shape='folder', style='filled', fillcolor='#D6B08E')
            
            with m.subgraph(name='cluster_docker') as d:
                d.attr(label='Docker Containers')
                d.node('mars_plex', 'Plex Server', **container_style)
                d.node('mars_filezilla', 'FileZilla Web App (FTP)', **container_style)

        # --- Device: Saturn (Windows PC) ---
        h.node('saturn', 'Saturn (Windows PC)', **pc_style) 

    # --- End-User Devices ---
    t.node('neptune', 'Neptune (MacBook Air)', **device_style)
    t.node('voyager', 'Voyager (iPhone)', **device_style)

# --- Define Data Flow and Connections (Edges with Labels) ---
# FIX 2: Removed explicit labels for the specified edges.
# 1. NFS MOUNT LINK (Blue, Bold, No Arrow)
dot.edge('pluto_nfs', 'mars_mount', style='bold', color='#007BFF', dir='none', penwidth='2', constraint='false') # Label removed

# 2. FTP CONNECTION (Red, Dashed, Default Arrow)
dot.edge('seedbox_ftp', 'mars_filezilla', label='FTP Protocol Connection', style='dashed', color='#DC3545')

# 3. STORAGE WRITE PATH (Orange, Bold, Normal Arrow)
dot.edge('mars_filezilla', 'mars_mount', label='Data Write Path (FileZilla to Mount)', style='bold', color='#FF8C00', penwidth='3', arrowhead='normal', constraint='false')

# 4. DATA SYNCHRONIZATION (Orange, Dashed, Normal Arrow)
dot.edge('mars_mount', 'pluto_nfs', style='dashed', color='#FF8C00', arrowhead='normal', constraint='false') # Label removed

# 5. PLEX READ PATH (Green, Dashed, Default Arrow)
dot.edge('mars_plex', 'mars_mount', label='Media Stream Read', style='dashed', color='#28A745', constraint='false')

# ----------------------------------------------------------------------------------------
# --- ABSOLUTE BOTTOM RANKER ---
dot.node('absolute_bottom_ranker', '', shape='plaintext', width='0', height='0')
dot.edge('voyager', 'absolute_bottom_ranker', style='invis', weight='1000') 
dot.edge('saturn', 'absolute_bottom_ranker', style='invis', weight='1000') 

## 📐 Legend (Horizontal at the absolute bottom)
# ----------------------------------------------------------------------------------------
with dot.subgraph(name='cluster_legend') as leg:
    leg.attr(style='filled', color='#555555', fillcolor='#FFFFF0', peripheries='0', label='')

    leg.node('desc_title', 'Legend', shape='plaintext', fontsize='16')
    
    # Nodes for descriptions (horizontally aligned)
    leg.node('vis_A', '', shape='none', width='0.1', height='0.1')
    leg.node('desc_A', 'NFS v4 Link (Blue, Bold)', shape='plaintext')
    
    leg.node('vis_B', '', shape='none', width='0.1', height='0.1')
    leg.node('desc_B', 'FTP Protocol (Red, Dashed)', shape='plaintext')
    
    leg.node('vis_C', '', shape='none', width='0.1', height='0.1')
    leg.node('desc_C', 'Data Write Path (Orange, Bold)', shape='plaintext')
    
    leg.node('vis_D', '', shape='none', width='0.1', height='0.1')
    leg.node('desc_D', 'NFS Sync Write (Orange, Dashed)', shape='plaintext')
    
    leg.node('vis_E', '', shape='none', width='0.1', height='0.1')
    leg.node('desc_E', 'Media Stream Read (Green, Dashed)', shape='plaintext')
    
    # --- Horizontal Linking ---
    leg.edge('vis_A', 'desc_A', style='invis', weight='10')
    leg.edge('vis_B', 'desc_B', style='invis', weight='10')
    leg.edge('vis_C', 'desc_C', style='invis', weight='10')
    leg.edge('vis_D', 'desc_D', style='invis', weight='10')
    leg.edge('vis_E', 'desc_E', style='invis', weight='10')
    
    # Chain the elements horizontally
    leg.edge('desc_title', 'vis_A', style='invis')
    leg.edge('desc_A', 'vis_B', style='invis')
    leg.edge('desc_B', 'vis_C', style='invis')
    leg.edge('desc_C', 'vis_D', style='invis') 
    leg.edge('desc_D', 'vis_E', style='invis') 
    
    # Create the actual visible markers
    leg.edge('vis_A', 'vis_A', style='bold', color='#007BFF', dir='none', penwidth='2')
    leg.edge('vis_B', 'vis_B', style='dashed', color='#DC3545', dir='forward')
    leg.edge('vis_C', 'vis_C', style='bold', color='#FF8C00', penwidth='3', dir='forward')
    leg.edge('vis_D', 'vis_D', style='dashed', color='#FF8C00', dir='forward')
    leg.edge('vis_E', 'vis_E', style='dashed', color='#28A745', dir='forward')
    
    # Invisible edge from the absolute bottom ranker to the Legend's title
    dot.edge('absolute_bottom_ranker', 'desc_title', style='invis', constraint='true', weight='1000')

# ----------------------------------------------------------------------------------------

# Render the graph
dot.format = 'png'
dot.render('hybrid_cloud_architecture', view=True)

print("The graph title has been moved to the top, and the labels for the NFS Mount Link and NFS Sync Write edges have been removed. The Legend is now the absolute lowest visual element. The image 'hybrid_cloud_architecture.png' will open automatically.")