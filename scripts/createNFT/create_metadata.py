from brownie import createNFT, network
from pathlib import Path
from metadata.rinkeby.sample_metadata import metadata_template
from scripts.helpful_scripts import get_player
import os, requests, json
from nba_api.stats.static import players
from nba_api.stats import endpoints
import pandas as pd

player_to_image_uri = {
    
}


def main():
    tx_createNFT = createNFT[-1]
    number_of_collectibles = tx_createNFT.tokenCounter()
    print(f"You have created {number_of_collectibles} NFTs")
    for tokenID in range(number_of_collectibles):
        player = get_player(tx_createNFT.tokenToPlayer(tokenID))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{tokenID}-{player}.json"
        )
        collectible_metadata = metadata_template
        
        player_dict = players.get_players()

        Lebron_James = [player for player in player_dict if player['full_name'] == "LeBron James"][0]
        Lebron_James_Id = Lebron_James['id']

        Devin_Booker = [player for player in player_dict if player['full_name'] == "Devin Booker"][0]
        Devin_Booker_Id = Devin_Booker['id']

        Mason_Plumlee = [player for player in player_dict if player['full_name'] == "Mason Plumlee"][0]
        Mason_Plumlee_Id = Mason_Plumlee['id']

        data = endpoints.leagueleaders.LeagueLeaders()
        df = data.league_leaders.get_data_frame()
        
        #print(df.loc[df['PLAYER_ID'] == Mason_Plumle
        # e_Id])
        
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["PLAYER"] = player

            index = df[df['PLAYER_ID'] == id].index
            collectible_metadata["Team"] = df['TEAM'].values[index].tolist()
            collectible_metadata["PTS"] = df['PTS'].values[index].tolist()
            collectible_metadata["AST"] = df['AST'].values[index].tolist()
            collectible_metadata["REB"] = df['REB'].values[index].tolist()
              
            image_path = "./img/" + player.lower().replace("_", "-") + ".jpeg"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
                
            image_uri = image_uri if image_uri else player_to_image_uri
            collectible_metadata["image"] = image_uri
            
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
    
                
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        print('BoB!!')
        return image_uri
    
            
