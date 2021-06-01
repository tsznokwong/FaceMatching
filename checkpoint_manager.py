import torch

def save_checkpoint(path, model, optimizer, train_loss_history, valid_loss_history, valid_loss, verbose = 1):
    if path == None:
      return
    state_dict = { \
      "model_state": model.state_dict(), \
      "optimizer_state": optimizer.state_dict(), \
      "valid_loss": valid_loss, \
      "train_loss_history": train_loss_history, \
      "valid_loss_history": valid_loss_history \
    }
    torch.save(state_dict, path)
    if verbose > 0:
      print(f"Model saved to {path}")

def load_checkpoint(path, model, optimizer = None, device = "cpu", verbose = 1):
    state_dict = torch.load(path, map_location=device)
    model.load_state_dict(state_dict["model_state"])
    if optimizer != None:
      optimizer.load_state_dict(state_dict["optimizer_state"])
    valid_loss = state_dict["valid_loss"]
    valid_loss_history = state_dict["valid_loss_history"]
    train_loss_history = state_dict["train_loss_history"]
    if verbose > 0:
      print(f"Model loaded from {path}, with Validation Loss: {valid_loss}")
    return train_loss_history, valid_loss_history, valid_loss
